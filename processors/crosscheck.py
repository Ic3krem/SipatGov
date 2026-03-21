import logging
from typing import List, Dict
import numpy as np
from difflib import SequenceMatcher
from config import DEVICE

logger = logging.getLogger(__name__)

class CrossCheckProcessor:
    """Cross-check AI model for comparing promises vs accomplishments"""
    
    def __init__(self):
        self.device = DEVICE
    
    def compare_promise_vs_accomplishment(self, promise: str, accomplishment: str) -> Dict:
        """Compare a promise against accomplishment"""
        try:
            similarity = self._calculate_similarity(promise, accomplishment)
            match_score = self._calculate_match_score(promise, accomplishment)
            
            status = self._determine_status(similarity, match_score)
            anomaly_score = self._calculate_anomaly_score(similarity, match_score)
            
            return {
                'promise': promise,
                'accomplishment': accomplishment,
                'similarity_score': round(similarity, 3),
                'match_score': round(match_score, 3),
                'status': status,  # fulfilled, partial, broken, delayed
                'anomaly_score': round(anomaly_score, 3),  # 0.0 to 1.0
                'details': self._generate_details(similarity, match_score)
            }
        except Exception as e:
            logger.error(f"Error in comparison: {str(e)}")
            return {'error': str(e)}
    
    def batch_cross_check(self, promises: List[str], accomplishments: List[str]) -> Dict:
        """Cross-check multiple promises against accomplishments"""
        results = []
        unmatched_promises = []
        unmatched_accomplishments = list(accomplishments)
        
        for promise in promises:
            best_match = None
            best_score = 0.0
            
            for accomplishment in accomplishments:
                similarity = self._calculate_similarity(promise, accomplishment)
                if similarity > best_score:
                    best_score = similarity
                    best_match = accomplishment
            
            if best_match and best_score > 0.3:
                results.append(self.compare_promise_vs_accomplishment(promise, best_match))
                unmatched_accomplishments.remove(best_match)
            else:
                unmatched_promises.append(promise)
        
        return {
            'comparisons': results,
            'matched_count': len(results),
            'unmatched_promises': unmatched_promises,
            'unmatched_accomplishments': unmatched_accomplishments,
            'summary': self._generate_summary(results)
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using SequenceMatcher"""
        if not text1 or not text2:
            return 0.0
        
        matcher = SequenceMatcher(None, text1.lower(), text2.lower())
        return matcher.ratio()
    
    def _calculate_match_score(self, promise: str, accomplishment: str) -> float:
        """Calculate semantic match score"""
        try:
            # Extract keywords from both
            keywords_promise = set(self._extract_keywords(promise))
            keywords_accomplishment = set(self._extract_keywords(accomplishment))
            
            if not keywords_promise:
                return 0.5
            
            overlap = keywords_promise.intersection(keywords_accomplishment)
            match_score = len(overlap) / len(keywords_promise)
            return min(1.0, match_score)
        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            return 0.0
    
    def _calculate_anomaly_score(self, similarity: float, match_score: float) -> float:
        """Calculate anomaly risk score (0.0 = good, 1.0 = bad)"""
        # Combine similarity and match score
        combined_score = (similarity + match_score) / 2.0
        
        # Invert: high similarity = low anomaly
        anomaly = 1.0 - combined_score
        
        return min(1.0, max(0.0, anomaly))
    
    def _determine_status(self, similarity: float, match_score: float) -> str:
        """Determine the status of promise fulfillment"""
        combined = (similarity + match_score) / 2.0
        
        if combined >= 0.8:
            return "fulfilled"
        elif combined >= 0.5:
            return "partial"
        elif combined >= 0.3:
            return "delayed"
        else:
            return "broken"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        import re
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        
        words = re.findall(r'\b\w{3,}\b', text.lower())
        keywords = [w for w in words if w not in stop_words]
        return keywords
    
    def _generate_details(self, similarity: float, match_score: float) -> Dict:
        """Generate detailed analysis"""
        return {
            'text_similarity': "High" if similarity >= 0.7 else "Medium" if similarity >= 0.4 else "Low",
            'keyword_match': "Strong" if match_score >= 0.7 else "Moderate" if match_score >= 0.4 else "Weak",
            'recommended_action': self._recommend_action(similarity, match_score)
        }
    
    def _recommend_action(self, similarity: float, match_score: float) -> str:
        """Recommend next action"""
        combined = (similarity + match_score) / 2.0
        
        if combined >= 0.8:
            return "No action needed - promise likely fulfilled"
        elif combined >= 0.5:
            return "Review details - partial fulfillment or delayed"
        elif combined >= 0.3:
            return "Investigate - significant mismatch detected"
        else:
            return "Critical review needed - possible broken promise"
    
    def _generate_summary(self, comparisons: List[Dict]) -> Dict:
        """Generate summary statistics"""
        if not comparisons:
            return {
                'fulfilled': 0,
                'partial': 0,
                'delayed': 0,
                'broken': 0,
                'average_anomaly_score': 0.0
            }
        
        status_counts = {}
        total_anomaly = 0.0
        
        for comp in comparisons:
            status = comp.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
            total_anomaly += comp.get('anomaly_score', 0.0)
        
        return {
            'fulfilled': status_counts.get('fulfilled', 0),
            'partial': status_counts.get('partial', 0),
            'delayed': status_counts.get('delayed', 0),
            'broken': status_counts.get('broken', 0),
            'average_anomaly_score': round(total_anomaly / len(comparisons), 3)
        }
    
    def detect_anomalies(self, data: List[Dict]) -> List[Dict]:
        """Detect anomalies in government promises/budgets"""
        anomalies = []
        
        try:
            for item in data:
                promise = item.get('promise', '')
                budget = item.get('budget', 0)
                accomplishment = item.get('accomplishment', '')
                
                comparison = self.compare_promise_vs_accomplishment(promise, accomplishment)
                anomaly_score = comparison.get('anomaly_score', 0.0)
                
                # Flag as anomaly if high risk
                if anomaly_score > 0.6:
                    anomalies.append({
                        'item': item,
                        'anomaly_score': anomaly_score,
                        'reason': comparison.get('details', {}).get('recommended_action', ''),
                        'severity': 'critical' if anomaly_score > 0.8 else 'high' if anomaly_score > 0.7 else 'medium'
                    })
            
            logger.info(f"Detected {len(anomalies)} anomalies")
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
        
        return anomalies
