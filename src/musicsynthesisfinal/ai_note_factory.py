from note_factory import NoteFactory
from sampling import top_p_sampling, temperature_sampling

from music21.converter import parseData
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import samplings


class AiNoteFactory(NoteFactory):
    def __init__(self, text, device='cpu'):
        self.device = torch.device(device)
        self.tokenizer = AutoTokenizer.from_pretrained(
            'sander-wood/text-to-music')
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            'sander-wood/text-to-music', device_map=device)
        self.model.eval()

        self.max_length = 1024
        self.top_p = 0.9
        self.temperature = 1.0

        self.input_ids = self.tokenizer(text,
                                        return_tensors='pt',
                                        truncation=True,
                                        max_length=self.max_length).to(self.device)['input_ids']

        self.decoder_start_token_id = self.model.config.decoder_start_token_id
        self.eos_token_id = self.model.config.eos_token_id

    def get_notes(self):
        decoder_input_ids = torch.tensor([[self.decoder_start_token_id]], device=self.device)

        for t_idx in range(self.max_length):
            outputs = self.model(input_ids=self.input_ids,
                                 decoder_input_ids=decoder_input_ids)
            # probs = outputs.logits[0][0][-1]
            probs = outputs[0][0][-1]
            sampled_id = prob_helper(
                probs, self.top_p, self.temperature)

            decoder_input_ids = torch.cat(
                (decoder_input_ids, sampled_id.reshape((1, 1))), 1)
            if sampled_id != self.eos_token_id:
                continue
            else:
                tune = "X:1\n"
                tune += self.tokenizer.decode(decoder_input_ids[0],
                                              skip_special_tokens=True)
                return parseData(tune, format="ABC")


def prob_helper(probs, top_p: float, temperature: float) -> torch.Tensor:
    probs = probs.softmax(dim=-1)
    tmp = top_p_sampling(probs.detach(), top_p=top_p, return_probs=True)
    result = temperature_sampling(tmp, temperature)
    return result
