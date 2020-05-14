create_schema = {
    'info': {
        'type': 'str',
        'minLength': 1,
        'maxLength': 200
    },
    'images': {
        'type': 'array',
        'items': {
            'type': 'str',
            'minLength': 1
        }
    },
    'required': ['info', 'images']
}

index_schema = {
	
}