package ro.ubbcluj.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import ro.ubbcluj.converter.ChildrenConverter;
import ro.ubbcluj.dto.ChildDTO;
import ro.ubbcluj.entity.Person;
import ro.ubbcluj.enums.RoleEnum;
import ro.ubbcluj.interfaces.ChildrenService;
import ro.ubbcluj.repository.PersonRepository;

import javax.transaction.Transactional;

/**
 * @author dianat2
 */
@Service
public class ChildrenServiceImpl implements ChildrenService {

    @Autowired
    private PersonRepository personRepository;

    @Override
    @Transactional
    public Page<ChildDTO> getAll(Pageable pageable) {
        final Page<Person> children = personRepository.findAllByRole_role(RoleEnum.PRESCHOOLAR, pageable);
        return ChildrenConverter.convertToDTOPage(children);
    }

}
