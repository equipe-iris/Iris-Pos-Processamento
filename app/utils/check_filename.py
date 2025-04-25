def check_filename(filename: str) -> bool:
    if not filename: return False

    if filename != 'Jira Exportar CSV (todos os campos) 20250312084318.csv' and filename != 'Chamados Porto.csv':
        return False
    
    return True