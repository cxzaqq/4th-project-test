package com.microsoftwo.bootproject.service;

import com.microsoftwo.bootproject.dto.CalculatorDTO;
import org.springframework.stereotype.Service;

@Service
public class CalculatorService {

    public int plusTwoNumbers(CalculatorDTO calculatorDTO) {

        return calculatorDTO.getNum1() + calculatorDTO.getNum2();
    }
}
