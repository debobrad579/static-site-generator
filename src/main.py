import os, shutil, sys

from block import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


def rmdir_recursive(dir: str):
    if not os.path.exists(dir): raise Exception(f"Directiory '{dir}' does not exist.")

    for path in os.listdir(dir):
        rel_path = os.path.join(dir, path)
        if os.path.isfile(rel_path):
            os.remove(rel_path)
            continue
        rmdir_recursive(rel_path)

    os.rmdir(dir)


def copy_content(src: str, dst: str):
    if not os.path.exists(src): raise Exception(f"Source directiory '{src}' does not exist.")
    if not os.path.exists(dst): raise Exception(f"Destination directory '{dst}' does not exist.")

    rmdir_recursive(dst)
    os.mkdir(dst)

    for path in os.listdir(src):
        rel_path = os.path.join(src, path)
        if os.path.isfile(rel_path):
            print(f"Copying {rel_path} to {dst}")
            shutil.copy(rel_path, dst)
            continue
        dst_path = os.path.join(dst, path)
        os.mkdir(dst_path)
        copy_content(rel_path, dst_path)


def extract_title(markdown: str):
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) != BlockType.HEADING: continue
        if block.startswith("# "): return block[1:].strip()
    raise Exception("No header found.")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        markdown = file.read()
        content = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)

        with open(template_path) as template_file:
            template = template_file.read()
            html = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

            with open(dest_path, "w") as dest_file:
                dest_file.write(html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    if not os.path.exists(dir_path_content): raise Exception("Content directory does not exist.")
    if not os.path.exists(dest_dir_path): os.mkdir(dest_dir_path)

    for path in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path.replace(".md", ".html"))
        if os.path.isfile(content_path): generate_page(content_path, template_path, dest_path, basepath)
        else: generate_pages_recursive(content_path, template_path, dest_path, basepath)


def main():
    basepath = sys.argv[0] or "/"
    copy_content("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
