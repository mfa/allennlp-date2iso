## date2iso

### about

Decodes all common dates in all languages known by Faker to **iso8601** dates.  
Example: ``2 agosto, 1912``  ->  ``1912-08-02``

rebuild of
https://github.com/datalogue/keras-attention
in AllenNLP 2.7+

### generate the data

```
python generate.py -t 500000 -v 10000 --all
```

``--all`` is all languages known by babel - otherwise only [en, de, fr, es] are used


### training

```
allennlp train configurations/baseline.json -s output/`date +%s`
```

#### with wandb

(needs [wandb-allennlp](https://github.com/dhruvdcoder/wandb-allennlp) 0.3.0+)
```
wandb sweep configurations/wandb_baseline.yaml
```
