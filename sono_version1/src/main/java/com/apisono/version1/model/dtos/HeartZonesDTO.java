package com.apisono.version1.model.dtos;

import lombok.Data;

@Data
public class HeartZonesDTO {
    private float caloriesOut;
    private int max;
    private int min;
    private int minutes;
    private String name;
}
