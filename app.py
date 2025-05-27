#app.py
import streamlit as st
import streamlit as st
from kg_api import get_knowledge_graph_list
from llm_utils import extract_entities_from_question
from cache import get_cached_result, set_cached_result
from dotenv import load_dotenv
import json

load_dotenv()
st.title("Wyszukiwarka słów kluczowych w zadanym tekście")

query = st.text_area("Wpisz tekst aby dowiedzieć coś więcej o znalezionych encjach")

if query:
    with st.spinner("Analiza zapytania i pobieranie danych..."):
        entities = extract_entities_from_question(query)

        if not entities:
            st.error("Nie udało się wyodrębnić encji z zapytania. Spróbuj sformułować pytanie inaczej.")
        else:
            st.success(f"Znalezione encje: {', '.join(entities)}")
            all_results = {}
            for entity in entities:
                st.markdown(f"## 🔍 Wyniki dla: **{entity}**")

                cached_results = get_cached_result(entity)
                if cached_results:
                    st.info("Wyniki pobrane z cache.")
                    results = cached_results
                else:
                    results = get_knowledge_graph_list(entity, limit=4)
                    set_cached_result(entity, results)

                all_results[entity] = results

                if not results:
                    st.warning("Brak wyników.")
                else:
                    for i, item in enumerate(results, start=1):
                        name = item.get("name", "Brak nazwy")
                        desc = item.get("description", "Brak opisu")
                        detailed = item.get("detailedDescription", {})
                        more = detailed.get("articleBody", "")
                        url = detailed.get("url", "")

                        st.markdown(f"### {i}. {name}")
                        st.markdown(f"**Opis:** {desc}")
                        if more:
                            st.markdown(f"{more[:300]}{'...' if len(more) > 300 else ''}")
                        if url:
                            st.markdown(f"[Czytaj więcej]({url})")
                        st.markdown("---")
            
            if all_results:
                st.markdown("### Pobierz wszystkie wyniki jako plik JSON:")
                json_data = json.dumps(all_results, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📁 Pobierz JSON",
                    data=json_data,
                    file_name="wyniki_knowledge_graph.json",
                    mime="application/json"
                )
