#include <iostream>
#include <vector>
#include <filesystem>
#include "include/inja.hpp"

nlohmann::ordered_json open_json_file(std::filesystem::path file_path) {
   
    nlohmann::ordered_json temp_json;
    std::ifstream map_file;
    map_file.open(file_path);
    if(map_file) {
        try {
            map_file >> temp_json;
        } catch (nlohmann::ordered_json::exception& ex){
            map_file.close();
            std::string json_error{"load_mappings - Nightmare"};
            json_error.append(ex.what());
        }
    }

    return temp_json;
}

nlohmann::ordered_json inja_templ8(nlohmann::ordered_json& globals_data, nlohmann::ordered_json& temp_json) {

    if ( temp_json.is_object() ) {
        nlohmann::ordered_json json_obj;
        for(const auto& [key, field] : temp_json.items())
            json_obj[key] = inja_templ8(globals_data, field);
        return json_obj;
    }
    else if(temp_json.is_string()) {
        try {
            std::string post_inja{inja::render(temp_json.get<std::string>(), globals_data)};
            post_inja = inja::render(post_inja, globals_data);
            return post_inja;    
        } catch (...) {
            std::cout << "Missing field" << std::endl;
        }
    }
    return temp_json;
}

int dump_md_html(nlohmann::ordered_json& map_data, nlohmann::ordered_json globals_data, std::string _ids_name) {
    
    std::vector indices{0, 0};
    globals_data["indices"] = indices;

    for(const auto& [path,data] : map_data.items()) {
        for(const auto& [key, field] : data.items()) {
            map_data[path][key] = inja_templ8(globals_data, field);
        }
    }
    
    return 0;
}

int output_json(nlohmann::ordered_json out_data, std::filesystem::path done_map_path) {

    std::ofstream map_file;
    map_file.open(done_map_path);
    if(map_file) {
        try {
            map_file << out_data.dump(4);
        } catch (nlohmann::ordered_json::exception& ex){
            std::string json_error{"load_mappings - it did not work : "};
            json_error.append(ex.what());
        }
    }

    return 0;
}

int main() {

    std::vector<std::string> ids_names{"magnetics", "pf_active", "pf_passive", "wall", "tf", "equilibrium", "summary"};
    for (const auto ids_name : ids_names) {

        std::filesystem::path base_map_path = std::filesystem::current_path() / "mappings" / ids_name;
        if ( !std::filesystem::is_directory(base_map_path) ) return 1;

        auto top_level_globals = open_json_file( std::filesystem::current_path() / "mappings" / "globals.json" );
        auto mappings = open_json_file(base_map_path / "mappings.json");
        auto globals = open_json_file(base_map_path / "globals.json");
        top_level_globals.update(globals);

        const auto out_path{ std::filesystem::current_path() / "utils" / "gen_docs" / "out_mappings" / ids_name};
        if (!std::filesystem::is_directory(out_path) || !std::filesystem::exists(out_path)) {
            std::filesystem::create_directory(out_path);
        }

        dump_md_html(mappings, top_level_globals, ids_name);
        output_json(mappings, out_path / "mappings.json");
    }

    return 0;
}
