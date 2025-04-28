def check_filename(filename: str) -> bool:
    try:
        if not filename: raise ValueError("Filename cannot be empty")

        if filename != 'Jira Exportar CSV (todos os campos) 20250312084318.csv' and filename != 'Chamados Porto.csv':
            return False
        
        return True
    except Exception as e:
        raise Exception(f"Error checking filename: {e}")