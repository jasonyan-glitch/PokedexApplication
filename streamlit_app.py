import streamlit as st
from openai import OpenAI 
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
if "pokedex" not in st.session_state:
    st.session_state.pokedex = []

st.title("Pokemon Pokedex Generator")
st.subheader("Generate, save, view, and filter Pokemon entries.")
st.write("This website allows users to generate, save, and explore Pokémon Pokedex entries using AI.")
# This application generates a detailed Pokemon Pokedex entry based on a user-provided name, then saves it so users can view or filter previously generated Pokemon.

Question1 = st.text_input("""What do you want to do first?
1. add a pokemon
2. check the pokemon you have already added
3. check this type (ex: water, ghost, etc)
""")

if Question1 == "1":
    Question2 = st.text_input("what's the name of this pokemon?")

    if Question2:
        system="""
        You are a pokeman's pokedex.

        Return ONLY valid JSON. No markdown, no code blocks, no extra text.

        Always use this EXACT JSON shape:
        {
            "Ad":{
                "pokeman":{
                    "name":["...."],
                    "4 digit ID number":["..."],
                    "States":{
                        "Hp": ["..."],
                        "attack value": ["..."],
                        "defense value":["..."],
                        "speed value": ["..."]
                    },
                    "A description":["..."],
                    "Details":{
                        "Gender":["..."],
                        "Category":["..."],
                        "A list of abilities":["1. ...","2. ...","3. ..."]
                    },
                    "Types":["..."],
                    "A list of types that it's weak to":["..."],
                    "What it evolves to":["..."]
                }
            }
        }

        Rules: 
        Use the name that user input.
        You should give it 4 digit ID number.
        The value in the stats are all range.
        One pokeman may be one or two types.
        Write three abilities.
        """ 

        user_prompt = f"""
        name:{Question2}
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ]
        )

        data = json.loads(response.choices[0].message.content)
        pokemon = data["Ad"]["pokeman"]

        st.session_state.pokedex.append({
            "name": pokemon["name"][0],
            "ID": pokemon["4 digit ID number"][0],
            "Hp": pokemon["States"]["Hp"][0],
            "attack value": pokemon["States"]["attack value"][0],
            "defense value": pokemon["States"]["defense value"][0],
            "speed value": pokemon["States"]["speed value"][0],
            "A description": pokemon["A description"][0],
            "Gender": pokemon["Details"]["Gender"][0],
            "Category": pokemon["Details"]["Category"][0],
            "A list of abilities": pokemon["Details"]["A list of abilities"],
            "Types": pokemon["Types"],
            "Weak to": pokemon["A list of types that it's weak to"],
            "Evolves to": pokemon["What it evolves to"][0]
        })

        st.write("Name:", pokemon["name"][0])
        st.write("ID:", pokemon["4 digit ID number"][0])

        st.write("States:")
        st.write("Hp:", pokemon["States"]["Hp"][0])
        st.write("attack value:", pokemon["States"]["attack value"][0])    
        st.write("defense value:", pokemon["States"]["defense value"][0])
        st.write("speed value:", pokemon["States"]["speed value"][0])
        st.write("description:", pokemon["A description"][0])
        st.write("Types:", ", ".join(pokemon["Types"]))

        st.write("Detail:")
        st.write("Gender:", pokemon["Details"]["Gender"][0])
        st.write("Category:", pokemon["Details"]["Category"][0])
        st.write("A list of abilities:", pokemon["Details"]["A list of abilities"])

        st.write("Weak to:", ", ".join(pokemon["A list of types that it's weak to"]))
        st.write("Evolves to:", pokemon["What it evolves to"][0])

elif Question1 == "2":
    if st.session_state.pokedex == []:
        st.warning("You do not record pokemon.")
    else:
        for p in st.session_state.pokedex:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Name:", p["name"])
                st.write("ID:", p["ID"])
                st.write("HP:", p["Hp"])
                st.write("Attack:", p["attack value"])
                st.write("Defense:", p["defense value"])
                st.write("Speed:", p["speed value"])
                st.write("Description:", p["A description"])

            with col2:
                st.write("Gender:", p["Gender"])
                st.write("Category:", p["Category"])
                st.write("Abilities:", ", ".join(p["A list of abilities"]))
                st.write("Types:", ", ".join(p["Types"]))
                st.write("Weak to:", ", ".join(p["Weak to"]))
                st.write("Evolves to:", p["Evolves to"])

elif Question1 == "3":
    Question3 = st.text_input("Which types Pokemon do you check for")

    if Question3:
        a = False 
        for p in st.session_state.pokedex:
            if Question3 in p["Types"]:
                st.write(p["name"], p["ID"])
                a = True
        if not a:
            st.warning("you do not record this types pokemon before")

if st.button("Generate"):

    if Question1 != "1" and Question1 != "2" and Question1 != "3":
        st.warning("????? Wrong input")







