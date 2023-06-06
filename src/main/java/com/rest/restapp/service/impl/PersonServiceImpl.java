package com.rest.restapp.service.impl;

import com.rest.restapp.model.Person;
import com.rest.restapp.service.PersonService;
import com.rest.restapp.util.PersonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class PersonServiceImpl implements PersonService {
    @Autowired
    private PersonRepository personRepository;
    @Override
    public void create(Person person) {
    personRepository.save(person);
    }

    @Override
    public List<Person> readAll() {
        return personRepository.findAll();
    }

    @Override
    public Person read(Long id) {
        return personRepository.getReferenceById(id);
    }

    @Override
    public boolean update(Person person, Long id) {
        if( personRepository.existsById(id)){
            person.setId(id);
            personRepository.save(person);
            return true;
        }
        return false;
    }

    @Override
    public boolean delete(Long id) {
        if(personRepository.existsById(id)){
            personRepository.deleteById(id);
            return true;
        }
        return false;
    }
}
