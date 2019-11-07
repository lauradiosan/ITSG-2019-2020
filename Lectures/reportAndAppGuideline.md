The report has to include details about:

**Team's members**
1. skills and rolls
2. performed tasks (Gannt diagram)

**Data**
1. How the data was collected?
2. How the data was stored? (please justify your choice)
- Data warehouse
- Data streams
- Data lake
- Data mesh
- other (which one)
3. How the data could be visualized and analysed?
- FACETS https://pair-code.github.io/facets/
- PyViz https://pyviz.org/
- Altair https://altair-viz.github.io/
- Embedded projector http://projector.tensorflow.org/
- Code examples: https://github.com/parulnith/Data-Visualisation-libraries
	
**Pipeline**
1. Versioning tools (general ones or some specialized ones?)
- Code versioning
i.	DVC https://dvc.org/ (a CLI tool)
ii.	Pachyderm https://www.pachyderm.io/open_source.html
iii.	MLflow Projects https://www.mlflow.org/docs/latest/projects.html  (API and CLI tool)
- Data versioning https://emilygorcenski.com/post/data-versioning/

2. SW design
- Type of the high-level architecture (e.g. Fixed or flexible, distributed or not, architectural pattern, etc.)
- Component/module coupling (low coupled / highly coupled)
- AI component serving (serializable - pickle, MLleap http://mleap-docs.combust.ml/ -, xml format – PMML http://dmg.org/pmml/v4-3/GeneralStructure.html, json format – PFA http://dmg.org/pfa/docs/motivation/ -, H2O (POJO object http://docs.h2o.ai/h2o/latest-stable/h2o-docs/productionizing.html), 
i.	Embedded component
ii.	Component as a [micro]service
iii.	Intelligent component published as data
iv. other (which one)
- details about training (static/off-line or dynamic/online
- details about inference (static or dynamic)

3.	SW pipeline
- Pipeline's diagram (in order to better visualise the most important steps and components of the project)
-	Iterative perspective (for AI component) – how do these iterations roll and how do they affect the SW developping process?

4.	SW code
-	Usage of external/specialized ML libraries or not
- Debugging and bug identification (how?)
- Testing (how? which components have been tested?)

5.	Model deployment
6.	Continuous delivery 
a.	Process
b.	Used tools 

**Philosofical aspects**
1. Social impact of your project & results
2. Ethics in your ML-based projects
3. Farness of your intelligent algorithm
- https://cloud.google.com/blog/products/ai-machine-learning/building-ml-models-for-everyone-understanding-fairness-in-machine-learning
- https://developers.google.com/machine-learning/fairness-overview



