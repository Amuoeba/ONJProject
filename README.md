# Natural language processing 2017/2018

## Semantic Relation Extraction and Classification in Scientific Papers

### Preface
I have selected a 2018 SemEval task on _"Semantic Relation Extraction and Classification in Scientific Papers"_ as a topic for my assignment. I have decided for this challenge because it greatly coincides with an idea which I have been brewing for quite some time, namely an intellegent sistem that is capable to suggest to scientists which future research steps are more promissing.

I graduated in the field of Biochemistry and towards the end of my studies I realised that biological (probably other too) sciences have a bit of a problem regarding the quantity and frequency of data production and its integration in to overall bio knowledge. Anotother problem arising from quantity of data and its relational complexity is that scientist working in the field usually can't follow rapid data generation and new discoveries wich might be corelated to their research. This leads to formation of _"knowledge bubles"_ which have no media for interaction. I see a solution in a highly capable AI with human-like generalization abilities. This task is a great starting point towards a more complex solution.

### Task overview
As mentioned in the preface, scientists are overwhelmed with a constant flow of new information and concepts, which makes it hard to have a good overview of whole scientific domain. The task is adressing this problem by focusing on semantic relation classification and extraction from scientific papers. semantic relations between concepts are important in complex search queries where scientists want to find research papers which addresed a certain problem in a certain way or when they want to find roots of a certain idea.

The task proposes subdivision of in to 3 subtasks:
1. Relation classification
    1. On manualy anotated data (clean)
    1. On automatically anotated data (noisy)
1. Relation extraction and classification

It allso provides an evaluation framework which enables us to see how individual steps solutions impact the overall performance of relation classification. Next we will explore subtasks, data and evaluation procedure in more detail.

### Data
The training data is given as 2 sets of 350 abstracts in a anotated **XML** format with a coresponding list of relation data
in plain **txt** format. The difference between towo sets of abastracts is that one set is manualy anotated while the anotation for the other one is produced automatically. Manualy anotated set is used in subtasks 1.1 and 2, automatically anotated set is used in subtask 1.2.

##### The task defines 6 types of relations that need to be identified in the text:
1. **USAGE**
    is an asymmetrical relation. It holds between two entities X and Y, where, for example:

    X is used for Y

    X is a method used to perform a task Y

    X is a tool used to process data Y

    X is a type of information/representation of information used by/in a system Y)

2. **RESULT** is an asymmetrical relation. It holds between two entities X and Y, where, for example: 

    X gives as a result Y (where Y is typically a measure of evaluation)

    X yields Y (where Y is an improvement or decrease)

    a feature of a system or a phenomenon X yields Y (where Y is an improvement or decrease)

 

3. **MODEL-FEATURE** is an asymmetrical relation. It holds between two entities X and Y, where, for example:

    X is a feature/an observed characteristic of Y

    X is a model of Y

    X is a tag(set) used to represent Y

 

4. **PART_WHOLE** is an asymmetrical relation. It holds between two entities X and Y, where, for example:

    X is a part, a component of Y

    X is found in Y

    Y is built from/composed of X  

 

5. **TOPIC** is an asymmetrical relation. It holds between two entities X and Y, where, for example:

    X deals with topic Y

    X (author, paper) puts forward Y (an idea, an approach)

 

6. **COMPARE** is a symmetrical relation. It holds between two entities X and Y, where:

    X is compared to Y (e.g. two systems, two feature sets or two results)

##### Below is the XML structure of an anotated abstract
```xml
<doc>
<text id="H01-1001">
<title>
Activity detection for information access to oral communication
</title>
<abstract>
<entity id="H01-1001.1">Oral communication</entity>
is ubiquitous and carries important information yet it is also time consuming to document. Given the development of
<entity id="H01-1001.2">storage media and networks</entity>
one could just record and store a
<entity id="H01-1001.3">conversation</entity>
for documentation. The question is, however, how an interesting information piece would be found in a
<entity id="H01-1001.4">large database</entity>
. Traditional
<entity id="H01-1001.5">information retrieval techniques</entity>
use a
<entity id="H01-1001.6">histogram</entity>
```
Each part of text that coresponds to a single entity is enclosed in the _"<entity></entity>"_ tag. In manualy anotated set these entities are determined by humans in automatically anotated set they are determined by an algorithm. Each abstract and entity have their own identification numbers _H01-1001_ for the abstract in the above example and _H01-1001.1_ for the first entity found in this abstract. The list of relations between entities defines the relation type and entities involved in the relation. The exact format can be seen below:
USAGE(H01-1001.5,H01-1001.7,REVERSE)
USAGE(H01-1001.9,H01-1001.10)
PART_WHOLE(H01-1001.14,H01-1001.15,REVERSE)
MODEL-FEATURE(H01-1017.4,H01-1017.5)
PART_WHOLE(H01-1041.3,H01-1041.4,REVERSE)
USAGE(H01-1041.8,H01-1041.9)
MODEL-FEATURE(H01-1041.10,H01-1041.11,REVERSE)
USAGE(H01-1041.14,H01-1041.15,REVERSE)
USAGE(H01-1042.1,H01-1042.3)
MODEL-FEATURE(H01-1042.10,H01-1042.11)
PART_WHOLE(H01-1049.3,H01-1049.4,REVERSE)
RESULT(H01-1058.2,H01-1058.4)
RESULT(H01-1058.9,H01-1058.10)
    
