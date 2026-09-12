# Experiment configuration

[Back to the project](../README.md)

| Read in this order | File | Meaning |
|---|---|---|
| 1 | [Parameter codebook](../docs/variables.json) | Names, meanings, endpoint directions and supporting instruments |
| 2 | [Parameters](parameters.json) | The ten parameter distributions |
| 3 | [Correlation matrix](correlation_matrix_R.json) | Dependencies used when sampling joint profiles |
| 4 | [Population means](population_means.json) | Reference values used by applicable studies |
| 5 | [Societal configurations](configurations.json) | Proposed context combinations; the file records their approval status |
| 6 | [Phase seeds](seeds.json) | Original phase-level random seeds |

Individual study manifests also record their own seeds and exact configuration.
Use those frozen manifests when reproducing a study; the phase seed file is not
a complete list of every later experiment.

This folder contains scientific inputs, not display preferences. The naming pass
does not change any JSON file. Parameter codes and existing source paths stay fixed.
