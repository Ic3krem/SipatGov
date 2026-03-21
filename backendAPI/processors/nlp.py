import logging
from typing import List, Dict
import json
from config import DEVICE, NLP_MODEL, ENTITY_MODEL

logger = logging.getLogger(__name__)

class NLPProcessor:
    """NLP processor for extracting promises, budgets, and entities"""
    
    def __init__(self):
        self.device = DEVICE
        self.nlp_model_name = NLP_MODEL
        self.entity_model_name = ENTITY_MODEL
        self.init_models()
    
    def init_models(self):
        """Initialize NLP models"""
        try:
            from transformers import pipeline
            
            # Summarization/Classification model
            self.classifier = pipeline(
                "zero-shot-classification",
                model=self.nlp_model_name,
                device=0 if self.device == "cuda" else -1
            )
            logger.info(f"NLP classifier initialized: {self.nlp_model_name}")
            
            # Named Entity Recognition
            self.ner = pipeline(
                "ner",
                model=self.entity_model_name,
                aggregation_strategy="simple",
                device=0 if self.device == "cuda" else -1
            )
            logger.info(f"NER model initialized: {self.entity_model_name}")
        except Exception as e:
            logger.error(f"Error initializing NLP models: {str(e)}")
            self.classifier = None
            self.ner = None
    
    def extract_promises(self, text: str) -> List[Dict]:
        """Extract project promises from text"""
        promises = []
        try:
            sentences = self._split_sentences(text)
            
            candidate_labels = [
                "government promise",
                "project commitment",
                "budget allocation",
                "infrastructure project",
                "social program",
                "not a promise"
            ]
            
            for sentence in sentences[:20]:  # Limit processing
                if len(sentence.strip()) < 10:
                    continue
                
                result = self.classifier(sentence, candidate_labels, multi_class=True)
                
                top_label = result['labels'][0]
                confidence = result['scores'][0]
                
                if confidence > 0.5 and top_label != "not a promise":
                    promises.append({
                        'text': sentence,
                        'type': top_label,
                        'confidence': round(confidence, 3),
                        'entities': self._extract_entities(sentence)
                    })
            
            logger.info(f"Extracted {len(promises)} promises from text")
            return promises
        except Exception as e:
            logger.error(f"Error extracting promises: {str(e)}")
            return []
    
    def extract_budget_amounts(self, text: str) -> List[Dict]:
        """Extract budget amounts and allocations"""
        import re
        
        budgets = []
        try:
            # Look for patterns like "PHP 10 million", "$5 billion", "100,000 pesos"
            patterns = [
                r'(?:PHP|₱|pesos?)\s*(?:[\d,]+(?:\.\d+)?)\s*(?:million|billion|thousand|m|b|k)?',
                r'(?:USD?\s*)?[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|thousand|m|b|k))?',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    budgets.append({
                        'text': match.group(),
                        'position': match.start(),
                        'context': text[max(0, match.start()-50):match.end()+50]
                    })
            
            logger.info(f"Extracted {len(budgets)} budget amounts")
            return budgets[:10]  # Limit results
        except Exception as e:
            logger.error(f"Error extracting budgets: {str(e)}")
            return []
    
    def extract_timelines(self, text: str) -> List[Dict]:
        """Extract project timelines and dates"""
        import re
        from datetime import datetime
        
        timelines = []
        try:
            # Date patterns
            date_patterns = [
                r'\d{1,2}/\d{1,2}/\d{2,4}',
                r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}',
                r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
                r'Q[1-4]\s+\d{4}',
            ]
            
            for pattern in date_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    timelines.append({
                        'date_text': match.group(),
                        'position': match.start(),
                        'context': text[max(0, match.start()-50):match.end()+50]
                    })
            
            logger.info(f"Extracted {len(timelines)} timeline mentions")
            return timelines[:15]  # Limit results
        except Exception as e:
            logger.error(f"Error extracting timelines: {str(e)}")
            return []
    
    def extract_entities(self, text: str) -> Dict:
        """Extract named entities"""
        try:
            if self.ner is None:
                logger.warning("NER model not initialized")
                return {}
            
            entities = self.ner(text[:512])  # Limit input length
            
            entity_dict = {}
            for ent in entities:
                ent_type = ent['entity_group']
                if ent_type not in entity_dict:
                    entity_dict[ent_type] = []
                
                entity_dict[ent_type].append({
                    'word': ent['word'],
                    'score': round(ent['score'], 3)
                })
            
            logger.info(f"Extracted entities: {list(entity_dict.keys())}")
            return entity_dict
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {}
    
    def _extract_entities(self, text: str) -> Dict:
        """Helper to extract entities from a sentence"""
        try:
            if self.ner is None:
                return {}
            
            entities = self.ner(text[:256])
            entity_dict = {}
            for ent in entities[:5]:  # Limit to top 5
                ent_type = ent['entity_group']
                if ent_type not in entity_dict:
                    entity_dict[ent_type] = []
                entity_dict[ent_type].append(ent['word'])
            
            return entity_dict
        except Exception as e:
            return {}
    
    def process_document(self, text: str) -> Dict:
        """Process entire document and extract all information"""
        return {
            'promises': self.extract_promises(text),
            'budgets': self.extract_budget_amounts(text),
            'timelines': self.extract_timelines(text),
            'entities': self.extract_entities(text)
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
