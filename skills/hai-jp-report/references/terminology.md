# Terminology defaults

Use an approved glossary first. These are contextual starting points, not an official RP terminology standard. Do not force a preferred word when it changes meaning.

| Vietnamese / English | Japanese starting point | Context |
|---|---|---|
| IMP / EE | IMP / EE | Keep abbreviation; do not invent expansion or scoring model. |
| giả thuyết / hypothesis | 仮説 | Do not turn into a finding. |
| bằng chứng / evidence | 根拠; 証拠 where appropriate | 根拠 often suits business judgments; preserve evidence type. |
| chưa kiểm chứng / unverified | 未検証; 確認できていない | Distinguish missing testing from missing confirmation. |
| khách hàng mục tiêu / target customer | 対象顧客 | Preserve the segment and organization/person distinction. |
| sẵn sàng trả tiền / willingness to pay | 支払意思 | Distinguish ability, contract, and actual payment. |
| khách hàng trả phí / paying customer | 有料顧客 | Do not infer company/person counting units. |
| doanh thu / revenue | 売上高 | Not profit or cash flow. |
| lợi nhuận gộp / gross profit | 売上総利益 | Not operating profit or margin rate. |
| biên lợi nhuận gộp / gross margin | 売上総利益率 | Only when the source means a rate. |
| tính khả thi kỹ thuật / technical feasibility | 技術的な実現可能性 | Not business viability. |
| business viability | 事業としての成立可能性 | Preserve commercial/economic context. |
| thử nghiệm nhỏ / limited pilot | 小規模な試験導入 | Preserve limits and approval conditions. |
| PoC / proof of concept | PoC; 概念実証 | Follow approved label; no implied commercial launch. |
| khuyến nghị / recommendation | 提言; 推奨 | Not an approved decision. |
| quyết định / decision | 決定; 判断 | Preserve actor, scope, and effective status. |
| tạm hoãn / defer | 延期; 判断を保留 | Delayed execution differs from withheld judgment. |
| dừng / stop | 中止; 停止 | Project termination differs from temporary pause. |

## Report-specific glossary

Use [the TSV template](../assets/glossary-template.tsv) if the user wants a reusable glossary. Do not require one before translating. Maintain a working glossary for terms whose consistent interpretation matters.

Columns: `source_language`, `source_term`, `preferred_ja`, `avoid_ja`, `context`. Record the sense/domain. `avoid_ja` warns only for that sense, not globally. Empty cells are allowed.

Keep company/product names, source IDs, internal labels, and scores as supplied. Use a supplied official Japanese name; do not invent one. Preserve status codes such as a source's `GO` or `HOLD` unless the supplied schema defines Japanese labels.

Approved terminology outranks stylistic variety; source meaning still governs. Flag a material glossary conflict rather than mistranslating silently. Persist user corrections into a reusable glossary/style file only when requested.
