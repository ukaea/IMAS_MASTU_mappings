import json


def json_to_table(json_data):
    func_html_output = ''
    if not isinstance(json_data, dict):
        return func_html_output

    for ikey, ivalue in json_data.items():
        if ikey == "COMMENT":
            func_html_output += '<tfoot>'
            func_html_output += f'<tr><td colspan="2"><b><i>{ivalue}</i></b></td></tr>'
            func_html_output += '</tfoot>'
            continue
        func_html_output += '<tr>'
        func_html_output += f'<th><b>{ikey}</b></th>'
        if isinstance(ivalue, dict):
            func_html_output += '<td><table class="table table-bordered">'
            for jkey, jvalue in ivalue.items():
                func_html_output += '<tr>'
                func_html_output += f'<th><b>{jkey}</b></th>'
                func_html_output += f'<td>{jvalue}</td>'
                func_html_output += '</tr>'
            func_html_output += '</table></td>'

        else:
            func_html_output += f'<td>{ivalue}</td>'

        func_html_output += '</tr>'

    return func_html_output


if __name__ == '__main__':

    ids_list = ["magnetics", "pf_active", "pf_passive", "wall", "tf", "equilibrium", "summary"]

    input_path = "./utils/gen_docs/out_mappings"

    for ids_name in ids_list:
        with open(f"{input_path}/{ids_name}/mappings.json") as f:
            data = json.load(f)

        html_output = ''
        for key, value in data.items():
            html_output += '<table class="table table-bordered">'

            # Head
            html_output += f'<thead><td colspan="2"><b>{key}</b></td></thead>'

            # Body
            html_output += json_to_table(value)

            html_output += '</table>'
            html_output += '<br>'

        # ids_name = 'magnetics'
        with open(f'./docs/mappings/{ids_name}/mappings.md', 'w') as x:
            x.write(f"# {ids_name}\n")
            x.write(html_output)
