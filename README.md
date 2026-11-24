# GeoOOH 3.0 — aplicativo de inteligência geográfica

## Execução
Node.js 20+; sem dependências npm. `npm start` e abra `http://localhost:3000`.

O mapa usa Leaflet, tiles OpenStreetMap e Turf carregados por CDN. O servidor consulta Nominatim para geocodificação, Overpass para pontos de interesse e contém endpoint IBGE/SIDRA para população municipal (`/api/municipality?id=3519071`). É necessário acesso à internet. Para testar no iPhone na mesma rede Wi-Fi, abra `http://IP-LOCAL-DO-COMPUTADOR:3000` e libere o firewall. Para URL pública, implante o serviço Node em Render/Railway ou equivalente.

## Dados demográficos por raio
A API não possui automaticamente dados setoriais carregados. Baixe a malha **oficial e atualizada** do Censo 2022 no portal IBGE e confirme no dicionário os campos de população e domicílios. Instale Python geopandas e shapely e execute:

`python scripts/import_ibge.py /caminho/malha.gpkg --population-column CAMPO_POP --households-column CAMPO_DOM --municipality-prefix 3519071,3545803,3509502,3531803`

**Atenção:** os nomes CAMPO_POP e CAMPO_DOM são placeholders, não variáveis reais. Confira no dicionário. O arquivo gerado `data/sectors.geojson` será utilizado pelo servidor. A estimativa de população por círculo é feita pela razão da área de interseção de cada setor com o círculo. A hipótese de distribuição uniforme pode introduzir erros significativos, especialmente em setores não residenciais. Não há dados reais de sexo/idade/renda por círculo sem importação adicional.

## Tráfego
Para exibir contagens, crie `data/traffic.json` seguindo `data/traffic.example.json`, com `vehicles_per_day` numérico e origem verificável. O sistema usa a estação mais próxima a até 200 m, mas não garante mesma via ou sentido. **Não inventa fluxos nem horários.** Waze e Google Maps são links externos, não fontes de contagens diárias.

## Restrições e boas práticas
- Nominatim público: limite máximo de 1 consulta/segundo; servidor mantém cache, mas para produção multiusuário use serviço contratado ou hospedagem própria e identificação de aplicação com contato válido.
- Overpass público: uso moderado, disponibilidade variável. Para produção use instância própria/serviço contratado.
- OSM é colaborativo, portanto os estabelecimentos não representam todos os CNPJs existentes.
- Endpoint IBGE municipal disponível para integrações futuras; a interface evita confundir município com raio.
- A importação IBGE depende de arquivos oficiais fornecidos separadamente; o pacote não contém dados setoriais baixados.
- O serviço atual é um MVP, sem autenticação, banco espacial, rate limiting robusto, observabilidade ou testes de carga. Não exponha publicamente sem endurecimento.
