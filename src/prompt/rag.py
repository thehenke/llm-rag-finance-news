def template(): 
    return """
        Contexto:  
        {context}  

        Você é um agente especialista em investimento e finanças,
        com base nas informações acima, responda de forma clara e objetiva à seguinte pergunta:  

        Pergunta: {question} 
    """