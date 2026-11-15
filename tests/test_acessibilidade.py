def pagina(client):
    return client.get("/").get_data(as_text=True)


def test_pagina_declara_idioma_e_regiao_principal(client):
    html = pagina(client)
    assert '<html lang="pt-BR">' in html
    assert '<main id="conteudo"' in html


def test_pagina_tem_link_para_pular_ao_conteudo(client):
    assert 'href="#conteudo"' in pagina(client)


def test_pagina_oferece_controles_de_fonte_e_contraste(client):
    html = pagina(client)
    assert 'id="btn-fonte-mais"' in html
    assert 'id="btn-fonte-menos"' in html
    assert 'id="btn-contraste"' in html
    assert 'aria-pressed="false"' in html