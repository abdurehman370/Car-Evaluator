from evaluator import PriceEvaluator

def test_evaluator():
    # Mock results
    results = [
        {"price": 10000},
        {"price": 12000},
        {"price": 11000},
        {"price": 15000},
        {"price": 50000}, # Outlier
        {"price": 100},   # Placeholder/Outlier
        {"price": 11500},
        {"price": 13000},
    ]
    
    stats = PriceEvaluator.calculate_stats(results)
    
    print("Stats:", stats)
    
    assert stats['raw_count'] == 8
    assert stats['invalid_count'] == 1 # The 100 AED one
    assert stats['outlier_count'] == 1 # The 50000 AED one
    assert stats['total_evaluated'] == 6
    assert stats['min_price'] >= 500
    assert stats['max_price'] < 50000
    
    # Test deal evaluation
    deal = PriceEvaluator.evaluate_deal(11000, stats)
    print(f"Deal for 11000: {deal}")
    
    deal_over = PriceEvaluator.evaluate_deal(25000, stats)
    print(f"Deal for 25000: {deal_over}")

if __name__ == "__main__":
    test_evaluator()
    print("Verification tests passed!")
