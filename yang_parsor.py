import os
from pyang import context, repository, statements

def extra_node_info(leaf):
    info = {}
    space = '  '

    type_stmt = leaf.search_one('type')
    if type_stmt:
        info['type'] = type_stmt.arg

        # Enumeration values
        if type_stmt.arg == 'enumeration':
            enums = []
            for e in type_stmt.search('enum'):
                enum_name = e.arg
                enum_value = e.search_one('value').arg if e.search_one('value') else ''
                enum_desc = e.search_one('description').arg if e.search_one('description') else ''
                
                if enum_value:
                    if enum_desc:
                        enum_entry = f"{enum_name} (value={enum_value}, description={enum_desc})"
                    else:
                        enum_entry = f"{enum_name} (value={enum_value})"
                else:
                    if enum_desc:
                        enum_entry = f"{enum_name} (description={enum_desc})"
                    else:
                        enum_entry = f"{enum_name}"
                enums.append(enum_entry)
            if enums:
                info['enum'] = enums

        # Range or Length
        range_stmt = type_stmt.search_one('range') or type_stmt.search_one('length')
        if range_stmt:
            info['range/length'] = range_stmt.arg

        # Fraction-digits
        frac_stmt = type_stmt.search_one('fraction-digits')
        if frac_stmt:
            info['fraction-digits'] = frac_stmt.arg


    when_stmt = leaf.search_one('when')
    if when_stmt:
        info['when'] = when_stmt.arg
        
    # Units
    units_stmt = leaf.search_one('units')
    if units_stmt:
        info['units'] = units_stmt.arg

    # Mandatory
    mandatory_stmt = leaf.search_one('mandatory')
    if mandatory_stmt:
        info['mandatory'] = mandatory_stmt.arg

    # Config
    config_stmt = leaf.search_one('config')
    if config_stmt:
        info['config'] = config_stmt.arg

    # Status
    status_stmt = leaf.search_one('status')
    if status_stmt:
        info['status'] = status_stmt.arg

    # Default
    default_stmt = leaf.search_one('default')
    if default_stmt:
        info['default'] = default_stmt.arg

    # Description
    desc_stmt = leaf.search_one('description')
    if desc_stmt:
        info['description'] = desc_stmt.arg

    # if-feature
    feature_stmt = leaf.search_one('if-feature')
    if feature_stmt:
        info['if-feature'] = feature_stmt.arg

    return info

def extract_node_info(stmt, path="", module_name="", filename=""):
    current_path = f"{path}/{stmt.arg}" if path else stmt.arg
    entries = []

    if stmt.keyword == 'leaf':
        info = extra_node_info(stmt)

        leaf_type = info.get('type', 'unknown')
        description = info.get('description', 'N/A')

        entry = [
            f"1.Keypath: {current_path}",
            f"2.Type: leaf ({leaf_type})",
            f"3.Module: {module_name}",
            f"4.File: {filename}",
            f"5.Description: {description}"
        ]

        # 각각 따로 출력
        idx=6
        if 'if-feature' in info:
            entry.append(f"{idx}.if-feature: {info['if-feature']}")
            idx+=1
        if 'when' in info:
            entry.append(f"{idx}.when: {info['when']}")
            idx+=1
        if 'default' in info:
            entry.append(f"{idx}.Default: {info['default']}")
            idx+=1
        if 'units' in info:
            entry.append(f"{idx}.Units: {info['units']}")
            idx+=1
        if 'range/length' in info:
            entry.append(f"{idx}.Range/Length: {info['range/length']}")
            idx+=1
        if 'fraction-digits' in info:
            entry.append(f"{idx}.Fraction Digits: {info['fraction-digits']}")
            idx+=1
        if 'mandatory' in info:
            entry.append(f"{idx}.Mandatory: {info['mandatory']}")
            idx+=1
        if 'config' in info:
            entry.append(f"{idx}.Config: {info['config']}")
            idx+=1
        if 'status' in info:
            entry.append(f"{idx}.Status: {info['status']}")
            idx+=1
        if 'enum' in info:
            enum_vals = ', '.join(info['enum'])
            entry.append(f"{idx}.Enum: {enum_vals}")
            idx+=1

        entries.append('\n'.join(entry))

    elif stmt.keyword == 'list':
        description = stmt.search_one('description').arg if stmt.search_one('description') else 'N/A'
        key = stmt.search_one('key').arg if stmt.search_one('key') else ''

        entry = [
            f"1.Keypath: {current_path}",
            f"2.Type: list",
            f"3.Module: {module_name}",
            f"4.File: {filename}",
            f"5.Description: {description}"
        ]
        if key:
            entry.append(f"Key: {key}")

        entries.append('\n'.join(entry))

    elif stmt.keyword == 'leaf-list':
        description = stmt.search_one('description').arg if stmt.search_one('description') else 'N/A'
        key = stmt.search_one('key').arg if stmt.search_one('key') else ''

        entry = [
            f"1.Keypath: {current_path}",
            f"2.Type: leaf-list",
            f"3.Module: {module_name}",
            f"4.File: {filename}",
            f"5.Description: {description}"
        ]
        if key:
            entry.append(f"Key: {key}")

        entries.append('\n'.join(entry))


    elif stmt.keyword == 'container':
        description = stmt.search_one('description').arg if stmt.search_one('description') else 'N/A'
        entry = [
            f"1.Keypath: {current_path}",
            f"2.Type: container",
            f"3.Module: {module_name}",
            f"4.File: {filename}",
            f"5.Description: {description}"
        ]
        entries.append('\n'.join(entry))

    for child in getattr(stmt, 'i_children', []):
        print(f"child:{child.keyword}/{child.arg}")
        entries.extend(extract_node_info(child, current_path, module_name, filename))

    return entries
    
def get_source_code(filepath, line):
    """YANG 파일에서 특정 라인의 소스 코드 추출"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines[line-1].strip() if 0 < line <= len(lines) else "N/A"
    except Exception:
        return "N/A"

def extract_rpc_info(module, filename):
    entries = []
    for stmt in module.i_children:
        if stmt.keyword == 'rpc':
            description = stmt.search_one('description').arg if stmt.search_one('description') else ''
            feature = stmt.search_one('if-feature').arg if stmt.search_one('if-feature') else ''
            entry = [
                f"1.Name: {stmt.arg}",
                f"2.Type: RPC",
                f"3.Module: {module.arg}",
                f"4.File: {filename}",
                f"5.Description: {description or 'N/A'}"
            ]

            idx=6
            if feature:
                entry.append(f"{idx}.if-feature: {feature}")
                idx+=1

            # input 블록
            input_stmt = stmt.search_one('input')
            if input_stmt:
                input_fields = format_stmt_children(input_stmt, indent='  ')
                entry.append(f"{idx}.Input:")
                idx+=1
                if input_fields:
                    entry.extend(input_fields)
                else:
                    entry.append("  - (no input fields)")

            # output 블록
            output_stmt = stmt.search_one('output')
            if output_stmt:
                output_fields = format_stmt_children(output_stmt, indent='  ')
                entry.append(f"{idx}.Output:")
                idx+=1
                if output_fields:
                    entry.extend(output_fields)
                else:
                    entry.append("  - (no output fields)")

            

            entries.append('\n'.join(entry))

    return entries

def extract_section_from_description(description, keywords):
    if not description:
        return None

    lines = description.splitlines()
    result_lines = []
    in_section = False

    for line in lines:
        lower_line = line.lower()
        if any(kw in lower_line for kw in keywords):
            in_section = True
            result_lines.append(line.strip())
        elif in_section:
            if line.strip() == "":
                break
            result_lines.append(line.strip())

    return '\n'.join(result_lines) if result_lines else None


def format_stmt_children(stmt, indent='  '):
    lines = []
    for child in getattr(stmt, 'i_children', []):

        if stmt.keyword == 'type' and stmt.arg == 'enumeration':
            leaf_type = child.search_one('type').arg if child.search_one('type') else ''
            description = child.search_one('description').arg if child.search_one('description') else ''
            line = f"{indent}- {child.arg} (type: {leaf_type})"
            
            ######### 잘안됨
            # type_stmt = child.search_one('type')
            # enums = []
            # for e in type_stmt.search('enum'):
            #     enum_name = e.arg
            #     enum_value = e.search_one('value').arg if e.search_one('value') else ''
            #     enum_desc = e.search_one('description').arg if e.search_one('description') else ''
            #     print(f'RPC enum_name:{enum_name}')
            #     if enum_value:
            #         if enum_desc:
            #             enum_entry = f"{enum_name} (value={enum_value}, description={enum_desc})"
            #         else:
            #             enum_entry = f"{enum_name} (value={enum_value})"
            #     else:
            #         if enum_desc:
            #             enum_entry = f"{enum_name} (description={enum_desc})"
            #         else:
            #             enum_entry = f"{enum_name}"
            #     enums.append(enum_entry)

            # if enums:
            #     line += f"{enums}"

            if description:
                line += f" — {description}"
            lines.append(line)

        elif child.keyword == 'leaf':
            leaf_type = child.search_one('type').arg if child.search_one('type') else ''
            type_stmt = child.search_one('type')
            if type_stmt:
                leaf_range = type_stmt.search_one('range').arg if type_stmt.search_one('range') else ''
            description = child.search_one('description').arg if child.search_one('description') else ''
            
            line = f"{indent}- {child.arg} (type: {leaf_type}"

            if leaf_range:
                line += f", range:{leaf_range})"
            else:
                line += ")"

            if description:
                line += f" — {description}"

            lines.append(line)

        elif child.keyword == 'container':
            description = child.search_one('description').arg if child.search_one('description') else ''
            lines.append(f"{indent}- container {child.arg}: {description}")
            lines.extend(format_stmt_children(child, indent + '  '))

        elif child.keyword == 'list':
            key = child.search_one('key').arg if child.search_one('key') else ''
            description = child.search_one('description').arg if child.search_one('description') else ''
            if key:
                lines.append(f"{indent}- list {child.arg} (key: {key}) — {description}")
            else:
                lines.append(f"{indent}- list {child.arg} — {description}")
            lines.extend(format_stmt_children(child, indent + '  '))

        elif child.keyword == 'leaf-list':
            key = child.search_one('key').arg if child.search_one('key') else ''
            description = child.search_one('description').arg if child.search_one('description') else ''
            if key:
                lines.append(f"{indent}- leaf-list {child.arg} (key: {key}) — {description}")
            else:
                lines.append(f"{indent}- leaf-list {child.arg} — {description}")
            lines.extend(format_stmt_children(child, indent + '  '))

        elif child.keyword == 'uses':
            grouping = getattr(child, 'i_grouping', None)
            if grouping:
                lines.append(f"{indent}- uses {child.arg} (expands to:)")
                lines.extend(format_stmt_children(grouping, indent + '  '))

    return lines

def extract_notification_info(module, filename):
    entries = []
    for stmt in module.i_children:
        if stmt.keyword == 'notification':
            description = stmt.search_one('description').arg if stmt.search_one('description') else ''
            feature = stmt.search_one('if-feature').arg if stmt.search_one('if-feature') else ''
            
            #example = extract_section_from_description(description, ['example', '예:', '예제'])
            #format_info = extract_section_from_description(description, ['format', '형식'])

            entry = [
                f"1.Name: {stmt.arg}",
                f"2.Type: Notification",                
                f"3.Module: {module.arg}",
                f"4.File: {filename}",
                f"5.Description: {description or 'N/A'}"
            ]
            idx = 6
            if feature:
                entry.append(f"{idx}.if-feature: {feature}")
                idx+=1

            #if format_info:
            #    entry.append("Format:")
            #    entry.append(format_info)

            #if example:
            #    entry.append("Example:")
            #    entry.append(example)

            # 하위 필드 정보 (uses 포함)
            fields = format_stmt_children(stmt, indent='  ')
            if fields:
                entry.append(f"{idx}.Fields:")
                entry.extend(fields)

            entries.append('\n'.join(entry))

    return entries


def process_yang_directory(directory,
                           output_node='yang_output.txt',
                           output_rpc='yang_rpc.txt',
                           output_notif='yang_notification.txt'):
    repos = repository.FileRepository(directory)
    ctx = context.Context(repos)

    node_entries = []
    rpc_entries = []
    notif_entries = []

    for filename in os.listdir(directory):
        if filename.endswith('.yang'):
            file_path = os.path.join(directory, filename)
            print(f"{file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            try:
                module = ctx.add_module(filename, text)
                ctx.validate()
                module_name = module.arg

                node_entries.extend(extract_node_info(module, module_name=module_name, filename=filename))
                rpc_entries.extend(extract_rpc_info(module, filename))
                notif_entries.extend(extract_notification_info(module, filename))

            except Exception as e:
                print(f"에러 발생: {filename} - {e}")

    def write_entries(filepath, entries, label):
        with open(filepath, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(entry + '\n---\n')
        print(f"{label} {len(entries)}개 저장 완료: {filepath}")

    write_entries(output_node, node_entries, '노드 정보')
    write_entries(output_rpc, rpc_entries, 'RPC')
    write_entries(output_notif, notif_entries, 'Notification')


# 사용 예시
process_yang_directory('./oru')