package com.apisono.version1.model;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class,property = "id")
public class Heart  {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    //@Transient
    private User user;

    private LocalDate date;
    @OneToMany(mappedBy = "heart",cascade = CascadeType.ALL)
    private List<HeartZone> heartZoneList=new ArrayList<>();

    public void addHeartZone(HeartZone heartZone){
        this.heartZoneList.add(heartZone);
    }
}
