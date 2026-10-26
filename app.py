import streamlit as st
from storage import init_db, list_cards, add_card, update_card, delete_card

st.set_page_config(page_title='Kanban Board', layout='wide')
init_db()
st.title('Kanban Board')
with st.form('new_card', clear_on_submit=True):
    title=st.text_input('New card title')
    description=st.text_area('Description')
    priority=st.selectbox('Priority', ['low','medium','high'], index=1)
    if st.form_submit_button('Add card'):
        try:
            add_card(title,description,priority)
            st.rerun()
        except Exception as exc:
            st.error(f'Could not add card: {exc}')

cards=list_cards()
for col, (status, heading) in zip(st.columns(3), [('todo','To Do'),('doing','Doing'),('done','Done')]):
    with col:
        st.subheader(heading)
        for card in cards:
            if card['status'] != status:
                continue
            with st.expander(card['title']):
                with st.form(f"edit_{card['id']}"):
                    new_title=st.text_input('Title',card['title'])
                    new_desc=st.text_area('Description',card['description'])
                    new_priority=st.selectbox('Priority',['low','medium','high'],index=['low','medium','high'].index(card['priority']))
                    new_status=st.selectbox('Column',['todo','doing','done'],index=['todo','doing','done'].index(card['status']))
                    if st.form_submit_button('Save changes'):
                        try:
                            update_card(card['id'],new_title,new_desc,new_priority,new_status)
                            st.rerun()
                        except Exception as exc:
                            st.error(f'Could not update card: {exc}')
                if st.button('Delete card',key=f"delete_{card['id']}"):
                    delete_card(card['id'])
                    st.rerun()
