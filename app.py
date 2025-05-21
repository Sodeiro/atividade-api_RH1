
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empresa.db'
db = SQLAlchemy(app)

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    funcionarios = db.relationship('Funcionario', backref='departamento', lazy=True)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)

@app.route('/departamentos', methods=['POST'])
def criar_departamento():
    data = request.json
    novo = Departamento(nome=data['nome'])
    db.session.add(novo)
    db.session.commit()
    return jsonify({'id': novo.id, 'nome': novo.nome}), 201

@app.route('/departamentos', methods=['GET'])
def listar_departamentos():
    departamentos = Departamento.query.all()
    return jsonify([{'id': d.id, 'nome': d.nome} for d in departamentos])

@app.route('/departamentos/<int:id>', methods=['GET'])
def buscar_departamento(id):
    d = Departamento.query.get_or_404(id)
    return jsonify({'id': d.id, 'nome': d.nome})

@app.route('/departamentos/<int:id>', methods=['PUT'])
def atualizar_departamento(id):
    d = Departamento.query.get_or_404(id)
    data = request.json
    d.nome = data['nome']
    db.session.commit()
    return jsonify({'id': d.id, 'nome': d.nome})

@app.route('/departamentos/<int:id>', methods=['DELETE'])
def deletar_departamento(id):
    d = Departamento.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return '', 204

@app.route('/funcionarios', methods=['POST'])
def criar_funcionario():
    data = request.json
    novo = Funcionario(nome=data['nome'], cargo=data['cargo'], departamento_id=data['departamento_id'])
    db.session.add(novo)
    db.session.commit()
    return jsonify({'id': novo.id, 'nome': novo.nome, 'cargo': novo.cargo, 'departamento_id': novo.departamento_id}), 201

@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return jsonify([{'id': f.id, 'nome': f.nome, 'cargo': f.cargo, 'departamento_id': f.departamento_id} for f in funcionarios])

@app.route('/funcionarios/<int:id>', methods=['GET'])
def buscar_funcionario(id):
    f = Funcionario.query.get_or_404(id)
    return jsonify({'id': f.id, 'nome': f.nome, 'cargo': f.cargo, 'departamento_id': f.departamento_id})

@app.route('/funcionarios/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    f = Funcionario.query.get_or_404(id)
    data = request.json
    f.nome = data['nome']
    f.cargo = data['cargo']
    f.departamento_id = data['departamento_id']
    db.session.commit()
    return jsonify({'id': f.id, 'nome': f.nome, 'cargo': f.cargo, 'departamento_id': f.departamento_id})

@app.route('/funcionarios/<int:id>', methods=['DELETE'])
def deletar_funcionario(id):
    f = Funcionario.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    return '', 204

@app.route('/funcionarios_com_departamentos', methods=['GET'])
def listar_funcionarios_com_departamento():
    funcionarios = Funcionario.query.all()
    return jsonify([
        {'id': f.id, 'nome': f.nome, 'cargo': f.cargo, 'departamento': f.departamento.nome}
        for f in funcionarios
    ])

@app.route('/departamentos_com_funcionarios', methods=['GET'])
def listar_departamentos_com_funcionarios():
    departamentos = Departamento.query.all()
    return jsonify([
        {'departamento': d.nome, 'funcionarios': [{'id': f.id, 'nome': f.nome} for f in d.funcionarios]}
        for d in departamentos
    ])

@app.route('/funcionarios/<int:id>/departamento', methods=['GET'])
def departamento_de_funcionario(id):
    f = Funcionario.query.get_or_404(id)
    return jsonify({'id': f.id, 'nome': f.nome, 'departamento': f.departamento.nome})

@app.route('/departamentos/<int:id>/funcionarios', methods=['GET'])
def funcionarios_de_departamento(id):
    d = Departamento.query.get_or_404(id)
    return jsonify([{'id': f.id, 'nome': f.nome, 'cargo': f.cargo} for f in d.funcionarios])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
