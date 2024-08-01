import streamlit as st
import time
from extract import query_data, DEFAULT_PROMPT_TEMPLATE


def main():
    st.title("Flex A.I. Wise")

    st.header("Ask Your Question")
    question = st.text_input("Enter your Question:")
    prompt_template = st.text_area("Edit Prompt Template:", value=DEFAULT_PROMPT_TEMPLATE, height=200)

    if st.button("Submit"):
        with st.spinner("Processing your query..."):
            start_time = time.time()
            output1, output2 = query_data(question, prompt_template)
            end_time = time.time()
            elapsed_time = end_time - start_time

        st.success(f"Query processed in {elapsed_time:.2f} seconds")
        st.text_area("Output using Open A.I.", value=output2, height=200)
        st.text_area("Raw Results from Database", value=output1, height=150)


if __name__ == "__main__":
    main()