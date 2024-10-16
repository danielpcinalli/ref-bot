import util as ut

def test_split_lower_followed_by_upper():
    test_cases = [ # (input, exp_output)
        ('PALAVRA', 'PALAVRA'),
        ('variasPalavrasJuntas outras', 'varias Palavras Juntas outras'),
        ('Palavra', 'Palavra'),
        ('palavra', 'palavra'),
        ]

    for inp, exp_out in test_cases:
        assert exp_out == ut.split_lower_followed_by_upper(inp)
