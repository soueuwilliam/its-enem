#!/usr/bin/env python
"""
Script para carregar os dados do ENEM no formato JSONL e converter para
o formato usado pelo controller do sistema its-enem.

Suporta carregamento de dados tanto de arquivos locais quanto de URLs.
"""

from model.models import DomainModel, LearnerModel, PedagogyModel
from controller import Controller
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='Carregador de dados do ENEM para o sistema its-enem')
    parser.add_argument('--enem-file', default='data/enem_2024_09042025.jsonl', 
                        help='Caminho para o arquivo JSONL com dados do ENEM (local ou URL)')
    parser.add_argument('--domain-file', default='data/domain.yml',
                        help='Caminho para o arquivo YAML com o domínio')
    parser.add_argument('--pedagogy-file', default='data/pedagogy.yml',
                        help='Caminho para o arquivo YAML com a pedagogia')
    parser.add_argument('--num-learners', type=int, default=3,
                        help='Número de alunos simulados a serem gerados')
    parser.add_argument('--use-url', action='store_true',
                        help='Usar URL de exemplo em vez do arquivo local')
    args = parser.parse_args()

    # Carregar o modelo de domínio
    print(f"Carregando modelo de domínio de {args.domain_file}")
    domain_model = DomainModel(args.domain_file)
    
    # Se a flag --use-url foi fornecida, usar a URL de exemplo
    enem_source = args.enem_file
    if args.use_url:
        enem_source = "https://raw.githubusercontent.com/adaj/its-enem/main/data/enem_2024_09042025.jsonl"
        print(f"Usando dados do ENEM da URL: {enem_source}")
    else:
        print(f"Usando dados do ENEM do arquivo local: {enem_source}")
    
    # Converter dados do ENEM para o formato questions
    questions = domain_model.parse_enem_data(enem_source)
    print(f"Convertidas {len(questions)} questões do ENEM")
    
    # Mostrar exemplo da primeira questão convertida
    if questions:
        print("\nExemplo da primeira questão convertida:")
        print(json.dumps(questions[0], indent=2, ensure_ascii=False))
    else:
        print("\nNenhuma questão foi carregada. Verifique o arquivo ou URL de origem.")
        return
    
    # Carregar o modelo pedagógico
    print(f"\nCarregando modelo pedagógico de {args.pedagogy_file}")
    pedagogy_model = PedagogyModel(args.pedagogy_file)
    
    # Criar o controller com os dados carregados
    print("Criando controller com os dados carregados")
    controller = Controller(domain_model, pedagogy_model, questions)
    
    # Gerar e processar alunos simulados
    print(f"\nGerando {args.num_learners} alunos simulados")
    controller.generate_mock_reports(args.num_learners)

if __name__ == "__main__":
    main() 