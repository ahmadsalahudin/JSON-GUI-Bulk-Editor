import streamlit as st
import os
import json

st.set_page_config(page_title="Bulk JSON Editor", page_icon="📂")

# Helper functions

def load_json_files(directory):
    files = []
    paths = []
    if directory and os.path.isdir(directory):
        for fname in os.listdir(directory):
            if fname.endswith('.json'):
                path = os.path.join(directory, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    files.append(json.load(f))
                    paths.append(path)
    return files, paths


def save_json_files(files, paths):
    for data, p in zip(files, paths):
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def delete_key_recursive(node, key_to_delete, log, parent_key=None):
    found = False
    if isinstance(node, dict):
        if key_to_delete in node:
            log.append({'key_path': (parent_key or []) + [key_to_delete], 'value': node[key_to_delete]})
            del node[key_to_delete]
            found = True
        for k, v in list(node.items()):
            if delete_key_recursive(v, key_to_delete, log, (parent_key or []) + [k]):
                found = True
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if delete_key_recursive(v, key_to_delete, log, (parent_key or []) + [str(i)]):
                found = True
    return found


def remove_null_or_zero(node, log, parent_key=None, remove_key_only=False):
    if isinstance(node, dict):
        for k in list(node.keys()):
            v = node[k]
            if v in (0, None, "0", "00", [] if remove_key_only else 0) or (v == "" and remove_key_only):
                log.append({'key_path': (parent_key or []) + [k], 'value': v})
                del node[k]
            else:
                remove_null_or_zero(v, log, (parent_key or []) + [k], remove_key_only)
    elif isinstance(node, list):
        for i in range(len(node) - 1, -1, -1):
            v = node[i]
            if v in (0, None, "0", "00", [] if remove_key_only else 0) or (v == "" and remove_key_only):
                log.append({'key_path': (parent_key or []) + [str(i)], 'value': v})
                del node[i]
            else:
                remove_null_or_zero(v, log, (parent_key or []) + [str(i)], remove_key_only)


def display_log(log):
    for i, entry in enumerate(log, 1):
        st.write(f"{i}. Path: {' > '.join(entry['key_path'])} Deleted: {entry['value']}")


# Streamlit app
st.title("Bulk JSON Editor - Streamlit")

if 'json_files' not in st.session_state:
    st.session_state.json_files = []
    st.session_state.file_paths = []
    st.session_state.log = []

folder = st.text_input("JSON directory", "")
if st.button("Load JSON directory"):
    st.session_state.json_files, st.session_state.file_paths = load_json_files(folder)
    st.session_state.log = []
    st.success(f"Loaded {len(st.session_state.json_files)} JSON files")

if st.session_state.json_files:
    st.subheader("Preview of first file")
    st.json(st.session_state.json_files[0])

    if st.button("Remove null/zero values"):
        for data, path in zip(st.session_state.json_files, st.session_state.file_paths):
            remove_null_or_zero(data, st.session_state.log)
        st.success("Removed null/zero values")

    if st.button("Remove keys with null/zero values"):
        for data, path in zip(st.session_state.json_files, st.session_state.file_paths):
            remove_null_or_zero(data, st.session_state.log, remove_key_only=True)
        st.success("Removed keys with null/zero values")

    key_to_delete = st.text_input("Delete specific key")
    if st.button("Delete key") and key_to_delete:
        key_found = False
        for data, path in zip(st.session_state.json_files, st.session_state.file_paths):
            if delete_key_recursive(data, key_to_delete, st.session_state.log):
                key_found = True
        if key_found:
            st.success(f"Deleted key {key_to_delete}")
        else:
            st.info("Key not found")

    if st.button("Save JSON files"):
        save_json_files(st.session_state.json_files, st.session_state.file_paths)
        st.success("JSON files saved")

    st.subheader("Deletion Log")
    display_log(st.session_state.log)
    if st.button("Save log to deletion_log.txt"):
        if st.session_state.file_paths:
            directory = os.path.dirname(st.session_state.file_paths[0])
            log_path = os.path.join(directory, "deletion_log.txt")
            with open(log_path, 'w', encoding='utf-8') as f:
                for i, entry in enumerate(st.session_state.log, 1):
                    f.write(f"{i}. Path: {' > '.join(entry['key_path'])} Deleted: {entry['value']}\n")
            st.success(f"Log saved to {log_path}")
        else:
            st.error("No directory selected")

