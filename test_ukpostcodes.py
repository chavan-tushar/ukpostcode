import ukpostcodes

def test_validate_postcode():
    assert ukpostcodes.validate_postcode('EC1A 1BB') == True
    assert ukpostcodes.validate_postcode("W1A 0AX") == True
    # assert ukpostcodes.validate_postcode(" ") == False
    assert ukpostcodes.validate_postcode("QC1X 9EE") == True