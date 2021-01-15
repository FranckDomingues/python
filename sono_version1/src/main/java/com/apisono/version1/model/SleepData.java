package com.apisono.version1.model;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class,property = "id")
public class SleepData {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    private Sleep sleep;

    private int awakeCount;
    private int awakenDuration;
    private int awakeningsCount;
    private LocalDate dateOfSleep;
    private int duration;
    private int efficiency;
    private boolean isMainSleep;
    private int idLog;
    @OneToMany(mappedBy = "sleepData",cascade = CascadeType.ALL)
    private List<SleepMinuteData> minuteData=new ArrayList<>(); //esta é uma lista de muitos dataTime não sei que atribuir
    private int minutesAfterWakeup;
    private int minutesAsleep;
    private int minutesAwake;
    private int minutesToFallAsleep;
    private int restlessCount;
    private int restlessDuration;
    private LocalDate startTime;
    private int timeInBed;

    public void addSleepMinuteData(SleepMinuteData sleepMinuteData){
        minuteData.add(sleepMinuteData);
        sleepMinuteData.setSleepData(this);
    }
}
