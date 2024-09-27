#Import til at lave opgaverne 
from flask import Flask, jsonify, request
from data_dict_simple import simple
from data_dict import random_users
from member import data
import sqlite3
import requests 


app = Flask(__name__)

# Forbinelse til database "member.db"
def connect_db():
    conn = sqlite3.connect('member.db')
    return conn

app = Flask(__name__)


def get_github_repositories(username):
    token = "" #Indæst Github Token 
    headers = {'Authorization': f'token {token}'}
    response=requests.get(f'https://api.github.com/users/{username}/repos',headers=headers)
    

    if username == "": #Indsæt dit Github 
        response =requests.get(f'https://api.github.com/user/repos', headers=headers) 
    else: 
        response =requests.get(f'https://api.github.com/users/{username}/repos', headers=headers)
        
    if response.status_code == 200: 
        return response.json()  
    else:
        return [], 300

@app.route('/members', methods=['GET'])
def read_all():
    members = data()  
    members_with_repos = []

    for member in members:
        github_username = member.get('github_username')
        repositories = get_github_repositories(github_username)
        repo_names = [repo.get('name') for repo in repositories if isinstance(repo, dict)]
        members_with_repos.append({
            **member,
            'repositories': repo_names
        })

    return jsonify(members_with_repos), 200


@app.route('/members', methods=['POST'])
def create():
    data = request.get_json()
    simple.append(data)
    return jsonify(simple) 

#@app.route('/members/<github_username>',methods=['PUT'])
#def put(github_username):
    #update_data = request.get_json()
    #members=data()
    #for member in members:
        #if member['github_username'] == github_username:
            #member.update(data)
            #return jsonify({'message': 'members updated', 'student': member}), 200

@app.route('/members/delete/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        # Opret forbindelse til databasen
        with sqlite3.connect('member.db') as conn:
            cur = conn.cursor()

            # Tjek om medlemmet med det pågældende id findes
            cur.execute('SELECT * FROM members WHERE id = ?', (id,))
            member = cur.fetchone()

            if member is None:
                # Returner en 404-fejl, hvis medlemmet ikke findes
                return jsonify({"message": "Member not found"}), 404

            # Slet medlemmet fra databasen
            cur.execute('DELETE FROM members WHERE id = ?', (id,))
            conn.commit()  # Gem ændringerne

            # Returner en succes-besked
            return jsonify({"message": f"Member with id {id} deleted"}), 200

    except sqlite3.Error as e:
        # Håndtering af databasefejl
        return jsonify({"error": str(e)}), 500 

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_github(member_id):
    data=request.get_json
    new_github_username = request.json['github_username'] #skaffer nuværende username 

    if not new_github_username:
        return jsonify({'error': 'GitHub username is required'}), 400

   
    conn = connect_db()
    c = conn.cursor()

    
    c.execute('UPDATE members SET github_username = ? WHERE id = ?', (new_github_username, member_id))

   
    conn.commit()
    conn.close()

  
    return f"GitHub username for member {member_id} updated to {new_github_username}!", 200

app.run()