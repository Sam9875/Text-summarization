from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset,load_from_disk,load_metric
import torch
import pandas as pd
from textsummarizer.entity import ModelEvaluationConfig


def gemerate_batch_sized_chunks(self,list_of_elements,batch_size=32):
        """        Splits a list into smaller chunks of specified batch size.
        """       
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i + batch_size]

def calculate_metrics(self,datasets,metric,model,tokenizer,batch_size=16,device="cuda" if torch.cuda.is_available() else "cpu",
                          column_text="articles",column_summary="hghlights"):
        article_batches=list(self.gemerate_batch_sized_chunks(datasets[column_text],batch_size))
        summary_batches=list(self.gemerate_batch_sized_chunks(datasets[column_summary],batch_size))

        for article_batch,target_batch in tqdm(zip(article_batches,summary_batches),total=len(article_batches)):

            inputs=tokenizer(article_batch,max_length=1024,truncation=True,padding="max_length",return_tensors="pt")

            summaries =model.generate(
                input_ids=inputs["input_ids"].to(device),
                attention_mask=inputs["attention_mask"].to(device),
                length_penalty=0.8,
                num_beams=4,
                max_length=128)
            
            ''' parameter for length_penalty ensures that the model does not generate very long summaries'''

            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_spaces=True) for s in summaries]

            metric.add_batch(predictions=decoded_summaries, references=target_batch)

            #finaly compute the return ROUGE score
            score = metric.compute(use_stemmer=True)
            return score
        
def evaluate(self):
            device = "cuda" if torch.cuda.is_available() else "cpu"
            tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)

            # load the dataset
            datasets = load_from_disk(self.config.data_path)


            rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

            roufge_metric = load_metric('rouge')

            score = self.calculate_metric_on_test_ds(dataset_samsum_pt['test'][0:10],roufge_metric,model,tokenizer,batch_size=2,column_text="dialogue",column_summary="summary")

            rouge_dict=dict((rn,score[rn].mid.fmeasure) for rn in rouge_names)

            df =pd.DataFrame(rouge_dict,index=['pegasus'])
            df.to_csv(self.config.metrics_file_name,index=False)

