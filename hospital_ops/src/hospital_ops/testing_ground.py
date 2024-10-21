import os
from hospital_ops.common.constants import (
    HOSPITAL_GENERATED_COMMENTS_FOLDER_PATH,
    HOSPITAL_GOLD_COMMENTS_FOLDER_PATH,
)
import numpy as np
import pandas as pd
from ragas.metrics import (
    LLMContextRecall,
    Faithfulness,
    FactualCorrectness,
    SemanticSimilarity,
)
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas import SingleTurnSample, EvaluationDataset
from dotenv import load_dotenv

load_dotenv()

# Sample 1
sample1 = SingleTurnSample(
    user_input="What is the capital of Germany?",
    retrieved_contexts=["Berlin is the capital and largest city of Germany."],
    response="The capital of Germany is Berlin.",
    reference="Berlin",
)

# Sample 2
sample2 = SingleTurnSample(
    user_input="Who wrote 'Pride and Prejudice'?",
    retrieved_contexts=["'Pride and Prejudice' is a novel by Jane Austen."],
    response="'Pride and Prejudice' was written by Jane Austen.",
    reference="Jane Austen",
)

# Sample 3
sample3 = SingleTurnSample(
    user_input="What's the chemical formula for water?",
    retrieved_contexts=["Water has the chemical formula H2O."],
    response="The chemical formula for water is H2O.",
    reference="H2O",
)

sample4 = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    response="The Eiffel Tower is located in Paris.",
    reference="The Eiffel Tower is located in Paris.",
    retrieved_contexts=["Paris is the capital of France."],
)

sample4a = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    response="The Eiffel Tower is located in Paris.",
    reference="The Eiffel Tower is located in Paris.",
    retrieved_contexts=[
        "Paris is the capital of France. Berlin is the capital of Germany"
    ],
)

sample4b = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    response="The Eiffel Tower is located in Paris.",
    reference="The Eiffel Tower is located in Paris.",
    retrieved_contexts=[
        "Paris is the capital of France.",
        "Berlin is the capital of Germany.",
    ],
)

sample4c = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    response="The Eiffel Tower is located in Paris.",
    reference="The Eiffel Tower is located in Paris.",
    retrieved_contexts=[
        "Paris is the capital of France. Berlin is the capital of Germany. The Eiffel Tower completed in 1889 in Paris."
    ],
)


# with open(HOSPITAL_GENERATED_COMMENTS_FOLDER_PATH + "A.txt", "r") as file:
    # new_retrieved = file.read()
    # # custom_len = int(len(new_retrieved)/2) # Half
    # # custom_len = 3*int(len(new_retrieved)/4) # 3/4
    # custom_len = 94*int(len(new_retrieved)/100) # 4/5
    
    # new_retrieved = new_retrieved[:custom_len]
    # print(new_retrieved)
    # new_retrieved = '''
    # Community Hospital

    # 1. Beds: There was an increase in beds from 195 in February to 220 in May, with a slope of 10.00 and R-squared of 0.80, indicating an increase in capacity.

    # 2. Discharges: There is an upward trend in discharges from February to May, suggesting improved patient turnover or increased demand.
    # '''

with open(HOSPITAL_GENERATED_COMMENTS_FOLDER_PATH + 'A.txt', "r") as file:
    new_retrieved = []
    new_retrieved_line = file.readline()
    while (new_retrieved_line):
        if (new_retrieved_line.strip() != ""):
            new_retrieved.append(new_retrieved_line)
        new_retrieved_line = file.readline()

# with open(HOSPITAL_GOLD_COMMENTS_FOLDER_PATH + 'A_ragas.txt', "r") as file:
#     new_reference = file.read()

with open(HOSPITAL_GOLD_COMMENTS_FOLDER_PATH + "A.txt", "r") as file:
    new_reference = []
    new_reference_line = file.readline()
    while new_reference_line:
        new_reference.append(new_reference_line)
        new_reference_line = file.readline()

sample_list = []
print(len(new_reference))
print(len(new_retrieved))
for i in range(0, len(new_reference)):
    sample_list.append(
        SingleTurnSample(
            user_input="Analyse the hospital data",
            response=new_retrieved[i],
            reference=new_reference[i],
            retrieved_contexts=[new_retrieved[i]],
        )
    )


evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o", temperature=0))
dataset = EvaluationDataset(samples=sample_list)
metrics = [FactualCorrectness(mode="recall", atomicity="low", coverage="high")]
results = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=evaluator_llm,
)
df = results.to_pandas()
score_list = df['factual_correctness']
denominator = len(score_list)
numerator = np.sum(score_list[~np.isnan(score_list)])
# df.loc[len(df)] = ["","","",f"{numerator}/{denominator}"]
print(df.head(100))
print(f"TOTAL SCORE: {numerator}/{denominator}")
df.to_csv("./testing_result.csv")
