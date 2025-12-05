function normalizeText(s) {
  s = (s || '').toString();
  // remove acentos, lower, remove chars estranhos, compacta espaços
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
          .replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
}

function tokens(s) {
  const n = normalizeText(s);
  if (!n) return [];
  return n.split(' ').filter(Boolean);
}

/* Levenshtein simples (iterativo) */
function levenshtein(a, b) {
  a = (a||''); b = (b||'');
  if (a === b) return 0;
  const m = a.length, n = b.length;
  if (m === 0) return n;
  if (n === 0) return m;
  let v0 = Array.from({length: n+1}, (_,i)=>i);
  let v1 = new Array(n+1);
  for (let i=0;i<m;i++){
    v1[0] = i+1;
    for (let j=0;j<n;j++){
      const cost = a[i] === b[j] ? 0 : 1;
      v1[j+1] = Math.min(v1[j] + 1, v0[j+1] + 1, v0[j] + cost);
    }
    [v0,v1] = [v1,v0];
  }
  return v0[n];
}

// Pega duas strings e vê p quão semelhantes elas são (0 a 1)
function similarity(a,b){
  if (!a && !b) return 1;
  if (!a || !b) return 0;
  const dist = levenshtein(a,b);
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1;
  return 1 - (dist / maxLen);
}

// Constrói a lista de esportes normalizados
function buildNormalizedSports(sportMap) {
  return sportMap.map(item => {
    const value = item.value;
    const keys = (item.keys||[]).map(k => normalizeText(k));
    // incluir o próprio nome canônico como alternativa
    keys.push(normalizeText(value));
    // tokens do nome canônico (ex: "table_tennis" -> ["table","tennis"])
    keys.push(...normalizeText(value).split(' '));
    // dedupe
    const uniq = Array.from(new Set(keys.filter(Boolean)));
    return { value, keys: uniq };
  });
}

// Busca principal
function matchSport(query, normalizedSports) {
  const q = normalizeText(query);
  if (!q) return null;

  // remover stopwords antes (opcional)
  const STOPWORDS = new Set(['e','de','do','da','dos','das','em','no','na','nos','nas','um','uma','uns','umas','para','por','com','sem','ao','aos','à','às','quadra','campo','quadras','campos','esporte','esportes']);
  const qNoStop = q.split(' ').filter(t => !STOPWORDS.has(t)).join(' ') || q;

  // 1) exact match (a chave inteira corresponde)
  for (const m of normalizedSports) {
    if (m.keys.includes(qNoStop)) return m.value;
  }

  // 2) substring (ex: "campo de futebol" contém "futebol")
  for (const m of normalizedSports) {
    if (m.keys.some(k => qNoStop.includes(k))) return m.value;
  }

  // 3) token match (alguma palavra bate)
  const toks = qNoStop.split(' ').filter(Boolean);
  for (const m of normalizedSports) {
    if (m.keys.some(k => toks.includes(k))) return m.value;
  }

  // 4) fuzzy: similaridade máxima entre query e cada key
  let best = {value: null, score: 0};
  for (const m of normalizedSports) {
    for (const k of m.keys) {
      const sim = similarity(qNoStop, k);
      if (sim > best.score) { best = {value: m.value, score: sim}; }
    }
  }
  // limiar empírico: 0.55 — ajuste se quiser mais/menos permissivo
  return best.score >= 0.55 ? best.value : null;
}

const STOPWORDS = new Set(['e','de','do','da','dos','das','em','no','na','nos','nas','um','uma','uns','umas','para','por','com','sem',
    'ao','aos','à','às','quadra','campo','quadras','campos','esporte','esportes','público','publico','privado','privada','centro','centros',
    'esportivo','esportiva','esportivos','esportivas','clube','clubes','associação','associacao','sociedade','sociedades']);

function removeStopwords(s){
    return s.split(' ').filter(t=>!STOPWORDS.has(t)).join(' ');
}

const SPORT_MAP = [{ keys: ['tênis', 'tenis','quadra de tenis','quadra de tênis'], value: 'tennis' },
                { keys: ['basquete', 'basquetebol', 'basket','quadra de basquete'], value: 'basketball' },
                { keys: ['futebol', 'futsal', 'soccer', 'football','campo de futebol'], value: 'football' },
                { keys: ['voleibol', 'volei','quadra de volei'], value: 'volleyball' },
                { keys: ['atletismo'], value: 'athletics' },
                { keys: ['badminton'], value: 'badminton' },
                { keys: ['natacao', 'natação'], value: 'swimming' },
                { keys: ['basquete 3x3'], value: '3x3_basketball' },
                { keys: ['boxe'], value: 'boxing' },
                { keys: ['breaking','breakdance'], value: 'breaking' },
                { keys: ['canoagem de velocidade'], value: 'canoe_sprint' },
                { keys: ['canoagem slalom','canoagem'], value: 'canoe_slalom' },
                { keys: ['ciclismo bmx freestyle','ciclissmo freestyle','ciclismo bmx'], value: 'bmx_freestyle' },
                { keys: ['ciclismo bmx racing','ciclismo racing'], value: 'bmx_racing' },
                { keys: ['ciclismo de estrada','ciclismo estrada','ciclismo'], value: 'road_cycling' },
                { keys: ['ciclismo de pista','ciclismo pista'], value: 'track_cycling' },
                { keys: ['ciclismo mountain bike','ciclismo mtb','mountain bike'], value: 'mountain_biking' },
                { keys: ['escalada','escalada esportiva'], value: 'sport_climbing' },
                { keys: ['esgrima'], value: 'fencing' },
                { keys: ['ginastica artistica'], value: 'artistic_gymnastics' },
                { keys: ['ginastica de trampolim','ginastica trampolim'], value: 'trampoline_gymnastics' },
                { keys: ['ginastica ritmica'], value: 'rhythmic_gymnastics' },
                { keys: ['golfe'], value: 'golf' },
                { keys: ['handebol','handball','quadra de handebol'], value: 'handball' },
                { keys: ['hipismo salto','hipismo'], value: 'equestrian_jumping' },
                { keys: ['hóquei sobre grama','hockey sobre grama','hóquei grama','hockey grama'], value: 'field_hockey' },
                { keys: ['judô','judo'], value: 'judo' },
                { keys: ['jiu-jitsu','jiu jitsu'], value: 'jujitsu' },
                { keys: ['karatê','karate'], value: 'karate' },
                { keys: ['levantamento de peso','levantamento peso','levantamento'], value: 'weightlifting' },
                { keys: ['luta olímpica','luta olimpica','luta'], value: 'wrestling' },
                { keys: ['maratona aquatica','maratona aquática'], value: 'marathon_swimming' },
                { keys: ['nado artístico','nado artistico'], value: 'artistic_swimming' },
                { keys: ['natacao', 'natação'], value: 'swimming' },
                { keys: ['pentatlo moderno','pentatlo'], value: 'modern_pentathlon' },
                { keys: ['polo aquático','polo aquatico'], value: 'water_polo' },
                { keys: ['remo'], value: 'rowing' },
                { keys: ['rugby sevens','rugby 7s','rugby'], value: 'rugby_sevens' },
                { keys: ['saltos ornamentais','salto ornamental'], value: 'diving' },
                { keys: ['skateboarding','skate'], value: 'skateboarding' },
                { keys: ['surfe','surf'], value: 'surfing' },
                { keys: ['taekwondo'], value: 'taekwondo' },
                { keys: ['tenismo de mesa','tenis de mesa','ping pong'], value: 'table_tennis' },
                { keys: ['tiro com arco','tiro arco'], value: 'archery' },
                { keys: ['tiro esportivo','tiro'], value: 'shooting' },
                { keys: ['triatlo'], value: 'triathlon' },
                { keys: ['vela'], value: 'sailing' },
                { keys: ['voleibol de praia','volei de praia'], value: 'beach_volleyball' }
            ];
const SPORT_MAP_NORM = buildNormalizedSports(SPORT_MAP);

document.addEventListener('DOMContentLoaded', function () {
    console.log("Mapa carregou!");
    console.log("normalizeText:", normalizeText("TÊNIS"));
        const OVERPASS_ENDPOINTS = [
            'https://overpass-api.de/api/interpreter',
            'https://lz4.overpass-api.de/api/interpreter',
            'https://overpass.openstreetmap.ru/api/interpreter',
            'https://overpass.kumi.systems/api/interpreter'
        ];

        const brasilCenter = [-14.2350, -51.9253];
        const map = L.map('map', { zoomControl: true }).setView(brasilCenter, 4);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        L.control.scale().addTo(map);

        const markerLayer = L.layerGroup().addTo(map);

        const queryEl = document.getElementById('query');
        const searchBtn = document.getElementById('searchBtn');
        const clearBtn = document.getElementById('clearBtn');
        const resultsEl = document.getElementById('results'); // mantido, mas não será usado para listar
        const NORMALIZED_SPORTS = buildNormalizedSports(SPORT_MAP);

          function parseQueryToFilters(q) {
    const detected = matchSport(q, SPORT_MAP_NORM);
    const filters = [];
    if (detected) {
      filters.push(`["leisure"="pitch"]["sport"="${detected}"]`);
      filters.push(`["amenity"="sports_centre"]["sport"="${detected}"]`);
      filters.push(`["sport"="${detected}"]`);
    } else {
      filters.push(`["leisure"="pitch"]`);
      filters.push(`["amenity"="sports_centre"]`);
    }
    return filters;
    }


        function buildOverpassQL(filters, bbox) {
            let blocks = '';
            filters.forEach(f => {
                blocks += `node${f}(${bbox});\n`;
                blocks += `way${f}(${bbox});\n`;
                blocks += `relation${f}(${bbox});\n`;
            });
            return `[out:json][timeout:25];
(
${blocks}
);
out center;`;
        }

        function buildOverpassQLAround(filters, lat, lon, radius) {
            let blocks = '';
            filters.forEach(f => {
                blocks += `node${f}(around:${radius},${lat},${lon});\n`;
                blocks += `way${f}(around:${radius},${lat},${lon});\n`;
                blocks += `relation${f}(around:${radius},${lat},${lon});\n`;
            });
            return `[out:json][timeout:25];
(
${blocks}
);
out center;`;
        }

        function humanizeSport(s) {
            if (!s) return '';
            const k = s.toLowerCase();
            const map = { 'tennis': 'Tênis', 'football': 'Futebol', 'futsal': 'Futsal', 'basketball': 'Basquete', 'volleyball': 'Voleibol', 'soccer': 'Futebol' };
            return map[k] || s.charAt(0).toUpperCase() + s.slice(1);
        }

        function humanizeLeisure(l) {
            if (!l) return '';
            const k = l.toLowerCase();
            const map = { 'pitch': 'Quadra / Campo', 'sports_centre': 'Centro Esportivo', 'stadium': 'Estádio' };
            return map[k] || l;
        }

        function ensureUrlProtocol(u) {
            if (!u) return null;
            if (/^https?:\/\//i.test(u)) return u;
            return 'https://' + u;
        }

        function buildInfoUrl(tags, el) {
            if (!tags) tags = {};
            const site = tags.website || tags.url || tags['contact:website'];
            if (site) return ensureUrlProtocol(site);
            if (tags.wikipedia) {
                const parts = tags.wikipedia.split(':');
                if (parts.length >= 2) {
                    const lang = parts.shift();
                    const page = parts.join(':');
                    return `https://${lang}.wikipedia.org/wiki/${encodeURIComponent(page)}`;
                } else {
                    return `https://pt.wikipedia.org/wiki/${encodeURIComponent(tags.wikipedia)}`;
                }
            }
            if (el && el.type && el.id) return `https://www.openstreetmap.org/${el.type}/${el.id}`;
            return null;
        }

        function getOwnerLabel(tags) {
            if (!tags) return null;
            const keys = ['operator', 'owner', 'operator:owner', 'contact:owner', 'contact:website', 'owner:official'];
            for (const k of keys) if (tags[k]) return String(tags[k]).trim();
            return null;
        }

        function determineAccess(tags) {
            if (!tags) return { label: 'Desconhecido', css: 'access-unknown' };
            const access = (tags.access || tags['access:conditional'] || '').toLowerCase();
            if (access.includes('yes') || access.includes('public') || access.includes('open')) return { label: 'Público', css: 'access-open' };
            if (access.includes('no') || access.includes('private') || access.includes('restricted')) return { label: 'Privado/Restrito', css: 'access-closed' };
            const fee = (tags.fee || tags['fee'] || tags.charge || '').toLowerCase();
            if (fee && (fee.includes('yes') || fee.includes('paid') || fee.includes('ticket'))) return { label: 'Privado / Pago', css: 'access-closed' };
            const landuse = (tags.landuse || '').toLowerCase();
            if (['school', 'college', 'university', 'education'].includes(landuse)) return { label: 'Restrito (uso escolar)', css: 'access-closed' };
            const operator = (tags.operator || '').toLowerCase();
            const publicKeywords = ['prefeitura', 'municipal', 'município', 'cidade', 'secretaria', 'governo', 'city', 'municipalidad', 'department', 'pref'];
            if (publicKeywords.some(k => operator.includes(k))) return { label: 'Público', css: 'access-open' };
            const owner = (tags.owner || tags['operator:owner'] || '').toLowerCase();
            if (owner.includes('priv') || owner.includes('particular') || owner.includes('private')) return { label: 'Privado', css: 'access-closed' };
            const amen = (tags.amenity || '').toLowerCase();
            const leisure = (tags.leisure || '').toLowerCase();
            if (amen === 'park' || leisure === 'park' || amen === 'playground' || leisure === 'playground') return { label: 'Público', css: 'access-open' };
            if (tags.website || tags.phone || tags['contact:website']) return { label: 'Público (verificar)', css: 'access-open' };
            return { label: 'Desconhecido', css: 'access-unknown' };
        }

        async function tryPostOverpass(endpoint, body) {
            const res = await fetch(endpoint, {
                method: 'POST',
                body,
                headers: { 'Content-Type': 'text/plain' }
            });
            return res;
        }

        async function searchQuadras(queryText) {
            markerLayer.clearLayers();
            // status agora só em console / alert, não em lista visível
            console.log('Buscando quadras para:', queryText);

            const bounds = map.getBounds();
            let s = bounds.getSouth(), w = bounds.getWest(), n = bounds.getNorth(), e = bounds.getEast();
            let bbox = `${s},${w},${n},${e}`;

            const filters = parseQueryToFilters(queryText);
            let q = buildOverpassQL(filters, bbox);

            let lastError = null;
            const maxRetries = 3;
            for (let attempt = 0; attempt <= maxRetries; attempt++) {
                const endpoint = OVERPASS_ENDPOINTS[attempt % OVERPASS_ENDPOINTS.length];
                try {
                    const res = await tryPostOverpass(endpoint, q);
                    if (res.status === 504 || res.status === 502 || res.status === 522) {
                        lastError = new Error(`Overpass retornou ${res.status}`);
                        if (attempt < maxRetries) {
                            const shrinkFactor = 0.6 ** (attempt + 1);
                            const center = map.getCenter();
                            const latSpan = (n - s) * shrinkFactor / 2;
                            const lonSpan = (e - w) * shrinkFactor / 2;
                            s = center.lat - latSpan; n = center.lat + latSpan; w = center.lng - lonSpan; e = center.lng + lonSpan;
                            bbox = `${s},${w},${n},${e}`;
                            q = buildOverpassQL(filters, bbox);
                            continue;
                        }
                    } else if (!res.ok) {
                        lastError = new Error('Overpass retornou ' + res.status);
                    } else {
                        const data = await res.json();
                        renderOverpassResults(data);
                        return;
                    }
                } catch (err) {
                    lastError = err;
                    if (attempt < maxRetries) continue;
                }
            }

            // fallback: busca por raio progressivo no centro do mapa
            const center = map.getCenter();
            const radii = [2000, 5000, 10000];
            for (const r of radii) {
                for (const endpoint of OVERPASS_ENDPOINTS) {
                    try {
                        const q2 = buildOverpassQLAround(filters, center.lat, center.lng, r);
                        const res2 = await tryPostOverpass(endpoint, q2);
                        if (!res2.ok) continue;
                        const data2 = await res2.json();
                        if ((data2.elements || []).length > 0) {
                            renderOverpassResults(data2);
                            return;
                        }
                    } catch (e) {
                        continue;
                    }
                }
            }

            console.error('Busca falhou:', lastError);
            alert('Erro na busca: ' + (lastError ? lastError.message : 'timeout') + '. Tente reduzir a área visível ou centralizar o mapa e pesquisar novamente.');
        }

        // renderização dos resultados — apenas cria marcadores; sem lista abaixo do mapa
        function renderOverpassResults(data) {
            markerLayer.clearLayers();
            const elements = data.elements || [];
            if (elements.length === 0) {
                alert('Nenhuma quadra encontrada na área visível.');
                return;
            }

            elements.forEach((el) => {
                let lat, lon;
                if (el.type === 'node') { lat = el.lat; lon = el.lon; }
                else if ((el.type === 'way' || el.type === 'relation') && el.center) { lat = el.center.lat; lon = el.center.lon; }
                if (lat == null || lon == null) return;

                const tags = el.tags || {};
                const preferredName = tags['name:pt'] || tags.name || tags.ref || (tags['addr:street'] ? (tags['addr:street'] + (tags['addr:housenumber'] ? ' ' + tags['addr:housenumber'] : '')) : null);

                let title;
                if (preferredName) title = preferredName;
                else if (tags.sport) title = humanizeSport(tags.sport) + (tags.leisure ? ' — ' + humanizeLeisure(tags.leisure) : '');
                else if (tags.leisure) title = humanizeLeisure(tags.leisure);
                else title = 'Quadra pública';

                const popupParts = [];
                popupParts.push(`<strong>${escapeHtml(title)}</strong>`);
                if (tags.sport) popupParts.push('Esporte: ' + escapeHtml(humanizeSport(tags.sport)));
                if (tags.leisure) popupParts.push('Tipo: ' + escapeHtml(humanizeLeisure(tags.leisure)));
                if (tags.operator) popupParts.push('Operador: ' + escapeHtml(tags.operator));
                if (tags['addr:street']) popupParts.push('Endereço: ' + escapeHtml(tags['addr:street'] + (tags['addr:housenumber'] ? ', ' + tags['addr:housenumber'] : '')));
                if (tags.phone) popupParts.push('Telefone: ' + escapeHtml(tags.phone));
                if (tags.opening_hours) popupParts.push('Horário: ' + escapeHtml(tags.opening_hours));

                const ownerLabel = getOwnerLabel(tags);
                if (ownerLabel) popupParts.push('Dono/Operador: ' + escapeHtml(ownerLabel));
                else {
                    const accessInfo = determineAccess(tags);
                    popupParts.push(`<span class="${accessInfo.css}">Acesso: ${escapeHtml(accessInfo.label)}</span>`);
                }

                const infoUrl = buildInfoUrl(tags, el);
                if (infoUrl) popupParts.push(`<a href="${escapeHtml(infoUrl)}" target="_blank" rel="noopener noreferrer">Mais informações</a>`);
                else popupParts.push('<small>Fonte: OpenStreetMap</small>');

                const marker = L.marker([lat, lon]).addTo(markerLayer);
                marker.bindPopup(popupParts.join('<br>'));
                // informação só aparece quando o usuário clica no marcador (popup)
            });
        }

        function escapeHtml(s) {
            if (s == null) return '';
            return String(s).replace(/[&<>"']/g, function(m){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]; });
        }

        searchBtn.addEventListener('click', function () { searchQuadras(queryEl.value); });

        queryEl.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') { e.preventDefault(); searchQuadras(queryEl.value); }
        });

        clearBtn.addEventListener('click', function () { markerLayer.clearLayers(); queryEl.value = ''; });

        map.on('click', function (e) {
            L.popup().setLatLng(e.latlng).setContent(`Coordenadas: ${e.latlng.lat.toFixed(5)}, ${e.latlng.lng.toFixed(5)}`).openOn(map);
        });
    });