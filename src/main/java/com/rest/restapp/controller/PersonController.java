package com.rest.restapp.controller;

import com.rest.restapp.model.Person;
import com.rest.restapp.service.PersonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class PersonController {
    private PersonService personService;
    @Autowired
    public PersonController(PersonService personService) {
        this.personService = personService;
    }
    @PostMapping(value = "/persons")
    public ResponseEntity<?> create(@RequestBody Person person) {
        personService.create(person);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }
    @GetMapping(value = "/persons")
    public ResponseEntity<List<Person>> read() {
        final List<Person> persons = personService.readAll();

        return persons != null &&  !persons.isEmpty()
                ? new ResponseEntity<>(persons, HttpStatus.OK)
                : new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    @GetMapping(value = "/persons/{id}")
    public ResponseEntity<Person> read(@PathVariable(name = "id") long id) {
        final Person person = personService.read(id);

        return person != null
                ? new ResponseEntity<>(person, HttpStatus.OK)
                : new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    @PutMapping(value = "/persons/{id}")
    public ResponseEntity<?> update(@PathVariable(name = "id") long id, @RequestBody Person person) {
        final boolean updated = personService.update(person, id);

        return updated
                ? new ResponseEntity<>(HttpStatus.OK)
                : new ResponseEntity<>(HttpStatus.NOT_MODIFIED);
    }

    @DeleteMapping(value = "/persons/{id}")
    public ResponseEntity<?> delete(@PathVariable(name = "id") long id) {
        final boolean deleted = personService.delete(id);

        return deleted
                ? new ResponseEntity<>(HttpStatus.OK)
                : new ResponseEntity<>(HttpStatus.NOT_MODIFIED);
    }
}
