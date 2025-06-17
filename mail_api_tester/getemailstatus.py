import re
import dns.resolver
import json

def validar_email(email):
    """
    Valida a sintaxe do e-mail usando regex.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def verificar_mx(domain):
    """
    Verifica se o domínio tem registros MX válidos.
    """
    try:
        # Resolve os registros MX do domínio
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

def lambda_handler(event, context):
    """
    Função Lambda para lidar com a requisição HTTP.
    """
    # Pegando o e-mail da requisição
    email = event['queryStringParameters']['email']  # Espera que o e-mail esteja na query string
    
    # Validar a sintaxe do e-mail
    if not validar_email(email):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'E-mail inválido no formato'})
        }

    # Extrair o domínio do e-mail
    domain = email.split('@')[1]

    # Verificar se o domínio tem registros MX
    if not verificar_mx(domain):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Domínio não tem registros MX válidos'})
        }

    # Se a validação for bem-sucedida
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'E-mail válido'})
    }

