# Grilling topics

Use these topics to build the frontier. Skip a topic when the data or the files answer it.

| Topic | Example question |
|---|---|
| Useful action | Who gets the benefit of this project? Which decision or action changes for them? |
| Earlier runs | Which earlier runs does this run use? What is new in this run: data type, question, or a merge of runs? |
| Decision | What will you do differently for each possible answer? |
| Owner | Who makes the decision? Who reads the result? |
| Question | Which comparison answers the question? Which groups? |
| Population | Which samples are in scope? Which samples are out (normal tissue, metastasis, male, repeats)? |
| Endpoint | Which variable is the outcome? How is it measured? |
| Time origin | When does the clock start: diagnosis, treatment, or sample collection? Samples taken long after diagnosis (metastases, recurrences) need survival from sampling or a left-truncation correction. |
| Reference test | Which test is the truth for a classifier? Is it in the data? If not, what can the data show instead? |
| Measurement transfer | On which assay, lab, or platform will the decision be used? Results on research data do not transfer by themselves. |
| Design | Is there a batch, a site, a time effect? Are samples paired? |
| Controls | Which known effect must appear if the data is correct? It must not be the predictor, and it must not be computed from the predictor. The planner fixes the control. |
| Prior knowledge | Which published result must we reproduce or compare with? |
| Public or private | Is the asset under discussion (signature, method, data) already published? What does a license add? |
| Same variable twice | Two columns can record the same thing (two ER fields, two dates). Which one is the reference? |
| Success | Which number or figure ends the analysis? |
| Cost of error | What happens if the answer is wrong? Can the decision be reversed? |
| Delivery | When is the result due? Which format? |
| Resources | Do the time, the money, and the due date fit the method? |
