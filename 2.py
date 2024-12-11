import pickle
import streamlit as st

def load_schemas():
    try:
        with open('schemas.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def save_schemas(schemas):
    with open('schemas.pkl', 'wb') as f:
        pickle.dump(schemas, f)

def save_schema(name, schema):
    schemas = load_schemas()
    schemas[name] = schema
    save_schemas(schemas)

def delete_schema(name):
    schemas = load_schemas()
    if name in schemas:
        del schemas[name]
        save_schemas(schemas)
        return True
    else:
        return False

def merge_schemas(files):
    merged_schemas = load_schemas()
    for file in files:
        with open(file.name, 'rb') as f:
            schemas = pickle.load(f)
            for name, schema in schemas.items():
                if name in merged_schemas:
                    new_name = f"{name}_merged"
                    st.warning(f"Conflict for {name}. Renamed to {new_name}")
                    merged_schemas[new_name] = schema
                else:
                    merged_schemas[name] = schema
    save_schemas(merged_schemas)
    return merged_schemas

### Streamlit приложение

def main():
    st.title("Редактор Barfi-схем")

    # Sidebar для навигации
    menu = st.sidebar.radio("Меню", [
        "Создание схемы",
        "Список схем",
        "Просмотр схемы",
        "Удаление схемы",
        "Слияние схем"
    ])

    if menu == "Создание схемы":
        st.header("Создание схемы")
        name = st.text_input("Название схемы")
        schema_data = st.text_area("Данные схемы")
        if st.button("Сохранить"):
            save_schema(name, schema_data)
            st.success("Схема сохранена")

    elif menu == "Список схем":
        st.header("Список схем")
        schemas = load_schemas()
        for name in schemas.keys():
            st.write(name)

    elif menu == "Просмотр схемы":
        st.header("Просмотр схемы")
        schemas = load_schemas()
        schema_name = st.selectbox("Выберите схему", list(schemas.keys()))
        if schema_name:
            st.write(schemas[schema_name])

    elif menu == "Удаление схемы":
        st.header("Удаление схемы")
        schema_name = st.text_input("Название схемы для удаления")
        if st.button("Удалить"):
            if delete_schema(schema_name):
                st.success("Схема удалена")
            else:
                st.error("Схема не найдена")

    elif menu == "Слияние схем":
        st.header("Слияние схем")
        uploaded_files = st.file_uploader(
            "Выберите .barfi файлы",
            type=['barfi'],
            accept_multiple_files=True
        )
        if st.button("Объединить схемы"):
            if uploaded_files:
                merged_schemas = merge_schemas(uploaded_files)
                st.success("Схемы объединены")
            else:
                st.error("Не выбраны файлы для слияния")

if __name__ == "__main__":
    main()