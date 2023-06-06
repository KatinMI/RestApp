package com.rest.restapp.service;

import com.rest.restapp.model.Person;

import java.util.List;

public interface PersonService {
    void create(Person person);
    List<Person> readAll();
    Person read(Long id);
    boolean update(Person person, Long id);
    boolean delete(Long id);
}
