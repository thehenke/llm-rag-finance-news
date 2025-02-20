def template(): 
    return """
        Contexto:  
        {context}  

        Com base nas informações acima, responda de forma clara e objetiva à seguinte pergunta:  

        Pergunta: {question} 
    """