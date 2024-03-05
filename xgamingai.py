from openai import OpenAI
from prompt import PROMPT

client = OpenAI(api_key="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")

def get_next_action(data):
    health_npc = data["npc"]["_health"]
    id_npc = data["npc"]["id"]
    health_player = data["player"]["_health"]
    id_player = data["player"]["id"]
    enemies = data["enemy"]

    enemies_str = ""
    for enemy_id, enemy in enemies.items():
        enemies_str += f"{enemy_id} : {enemy}\n"

    prompt = PROMPT.format(
        health_npc=health_npc,
        id_npc=id_npc,
        health_player=health_player,
        id_player=id_player,
        enemies=enemies_str
    )

    print(prompt)

    result = client.chat.completions.create(model="gpt-3.5-turbo",
                                      messages=[
                                        {"role": "system", "content": prompt}
                                      ],
                                      functions=[
                                        {
                                            "name": "get_next_action", 
                                            "description": "Get the next action for the NPC",
                                            "parameters": {
                                                "name": "targets",
                                                "description": "The json object where entity_id is the id of the entity to cast the spell on and spell_id is the id of the spell to cast",
                                                "type": "object",
                                                "properties": {
                                                    "entity_id": {
                                                        "description": "The id of the entity to cast the spell on",
                                                        "type": "integer"
                                                    },
                                                    "spell_id": {
                                                        "description": "The id of the spell to cast",
                                                        "type": "integer"
                                                    },
                                                    "reason": {
                                                        "description": "The reason for casting the spell",
                                                        "type": "string"
                                                    }
                                                },

                                            },
                                        },
                                      ],
                                      function_call={"name": "get_next_action"}
    )

    targets = eval(result.choices[0].message.function_call.arguments)

    text_response = result.choices[0].message.content
    print(text_response)

    return targets


data = {
    "enemy": {
        "1": {
            "damage" : 100,
            "health" : 13,
            "distance" : 10,
        },
        "2": {
            "damage" : 10,
            "health" : 10,
            "distance" : 1,
        },
        "3": {
            "damage" : 1,
            "health" : 1000,
            "distance" : 7,
        }
    },
    "player": {
        "_health" : 1,
        "id" : 98
    },
    "npc": {
        "_health" : 100,
        "id" : 99
    }
}

print(get_next_action(data))