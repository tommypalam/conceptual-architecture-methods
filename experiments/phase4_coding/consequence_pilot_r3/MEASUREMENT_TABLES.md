# Independent rating inventory

One row per unique card and judge. Codes follow the frozen relative/fixed vector ordering.
Development expectations are authored diagnostic constraints, not human moral gold labels.

| Card | Judge | Relative vector | Fixed vector | Diagnostic constraints |
|---|---|---|---|---|
| disclosure_2/report | Claude | [0, 0, 0, 0, 1, 1, 1, 1] | [1, 1, 1, 1] | {} |
| disclosure_2/report | OpenAI | [0, 0, 0, 0, 1, 1, 1, 1] | [1, 1, 1, 1] | {} |
| disclosure_2/falsify | Claude | [0, 1, 1, 1, 0, 0, 0, 0] | [0, 0, 1, 1] | {} |
| disclosure_2/falsify | OpenAI | [0, 1, 1, 1, 0, 0, 1, 0] | [0, 0, 1, 1] | {} |
| disclosure_2/skip | Claude | [0, 1, 1, 1, 0, 0, 0, 0] | [0, 0, 1, 1] | {} |
| disclosure_2/skip | OpenAI | [0, 1, 1, 1, null, 0, 0, 0] | [0, 0, 1, 1] | {} |
| disclosure_12/report | Claude | [0, 0, 1, 0, 1, 1, 1, 1] | [1, 1, 1, 1] | {} |
| disclosure_12/report | OpenAI | schema invalid | schema invalid | {} |
| disclosure_12/falsify | Claude | [0, 1, 1, 1, 0, 0, 0, 0] | [0, 0, 1, 1] | {} |
| disclosure_12/falsify | OpenAI | [0, 1, 1, 1, 1, 0, 1, 0] | [0, 0, 1, 1] | {} |
| disclosure_12/skip | Claude | [0, 1, 1, 1, 0, 0, 0, 0] | [0, 0, 1, 1] | {} |
| disclosure_12/skip | OpenAI | [0, 1, 1, 1, 0, 0, 1, null] | [0, 0, 1, 1] | {} |
| allocation_6/equal | Claude | [0, 0, 0, 0, 1, 0, 1, 0] | [1, 1, 1, 1] | {} |
| allocation_6/equal | OpenAI | [0, 0, 0, 0, 1, 0, 1, 0] | [1, 1, 1, 1] | {} |
| allocation_6/unequal | Claude | [0, 0, 0, 1, 0, 0, 0, 0] | [1, 1, 1, 0] | {} |
| allocation_6/unequal | OpenAI | [0, 0, 0, 1, 1, 0, 1, 0] | [1, 1, 1, 0] | {} |
| allocation_6/skip | Claude | [0, 0, 1, 1, 0, 0, 0, 0] | [0, 1, 1, 1] | {} |
| allocation_6/skip | OpenAI | [0, 0, 1, 1, null, 0, 0, null] | [0, 1, 1, 0] | {} |
| allocation_12/equal | Claude | [0, 0, 0, 0, 1, 0, 1, 0] | [1, 1, 1, 1] | {} |
| allocation_12/equal | OpenAI | [0, 0, 0, 0, 1, 0, 1, 0] | [1, 1, 1, 1] | {} |
| allocation_12/unequal | Claude | [0, 0, 0, 1, 0, 0, 0, 0] | [1, 1, 1, 0] | {} |
| allocation_12/unequal | OpenAI | [0, 0, 0, 1, 1, 0, 1, 0] | [1, 1, 1, 0] | {} |
| allocation_12/skip | Claude | [0, 0, 1, 1, 0, 0, 0, 0] | [0, 1, 1, 0] | {} |
| allocation_12/skip | OpenAI | [0, 0, 1, 1, 0, 0, 0, 0] | [0, 1, 1, 0] | {} |
| development/regression 1 | Claude | [0, 0, 1, 0, 0, 0, 1, 1] | [1, 1, 1, 1] | {"configuration_relative": {"2": 1, "6": 1}, "fixed_standard": {"0": 1}} |
| development/regression 1 | OpenAI | [0, 0, 1, null, 0, 0, 1, null] | [1, 1, 1, 1] | {"configuration_relative": {"2": 1, "6": 1}, "fixed_standard": {"0": 1}} |
| development/regression 2 | Claude | schema invalid | schema invalid | {"configuration_relative": {"2": 0}, "fixed_standard": {"0": 0}} |
| development/regression 2 | OpenAI | [0, 0, 1, null, 0, 0, 1, 0] | [0, 1, 1, 1] | {"configuration_relative": {"2": 0}, "fixed_standard": {"0": 0}} |
| development/regression 3 | Claude | [0, 0, null, null, 0, 0, null, 0] | [null, 1, 1, 1] | {"configuration_relative": {"2": null}, "fixed_standard": {"0": null}} |
| development/regression 3 | OpenAI | [0, 0, null, null, 0, 0, null, null] | [null, 1, 1, 1] | {"configuration_relative": {"2": null}, "fixed_standard": {"0": null}} |
| development/regression 4 | Claude | [0, 0, 0, 0, 0, 0, 0, 0] | [1, 1, 1, 1] | {"configuration_relative": {"1": 0}, "fixed_standard": {"1": 1}} |
| development/regression 4 | OpenAI | [0, 0, 0, 0, null, 0, 0, 0] | [1, 1, 1, 1] | {"configuration_relative": {"1": 0}, "fixed_standard": {"1": 1}} |
| development/regression 5 | Claude | [0, 0, 0, 0, 0, 0, 0, 0] | [1, 1, 1, 1] | {"configuration_relative": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}, "fixed_standard": {"0": 1, "1": 1, "2": 1, "3": 1}} |
| development/regression 5 | OpenAI | [0, 0, 0, 0, 0, 0, 0, 0] | [1, 1, 1, 1] | {"configuration_relative": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}, "fixed_standard": {"0": 1, "1": 1, "2": 1, "3": 1}} |
| development/regression 6 | Claude | [null, 0, 0, null, null, 0, 0, 0] | [1, 1, 1, 1] | {"configuration_relative": {"0": null, "4": null}} |
| development/regression 6 | OpenAI | [1, 0, 0, null, null, 0, 0, 0] | [1, 1, 1, 1] | {"configuration_relative": {"0": null, "4": null}} |
| development/regression 7 | Claude | [0, 1, 0, 1, 0, 0, 0, 0] | [1, 0, 1, 1] | {"configuration_relative": {"1": 1}, "fixed_standard": {"1": 0}} |
| development/regression 7 | OpenAI | [0, 1, 0, 1, 0, 0, 0, 0] | [1, 0, 1, 1] | {"configuration_relative": {"1": 1}, "fixed_standard": {"1": 0}} |
| development/regression 8 | Claude | [0, 0, 0, 1, 0, 0, 0, 0] | [1, 1, 0, 1] | {"configuration_relative": {"3": 1}, "fixed_standard": {"2": 0}} |
| development/regression 8 | OpenAI | [0, 0, 0, 1, null, 0, 1, null] | [1, 1, 0, 1] | {"configuration_relative": {"3": 1}, "fixed_standard": {"2": 0}} |
