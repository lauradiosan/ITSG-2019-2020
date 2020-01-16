package ro.ubbcluj.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.ObjectUtils;
import ro.ubbcluj.converter.UserConverter;
import ro.ubbcluj.dto.ChildDTO;
import ro.ubbcluj.dto.UserDTO;
import ro.ubbcluj.entity.Account;
import ro.ubbcluj.entity.Person;
import ro.ubbcluj.enums.RoleEnum;
import ro.ubbcluj.interfaces.UserService;
import ro.ubbcluj.repository.AccountRepository;
import ro.ubbcluj.repository.PersonRepository;
import ro.ubbcluj.repository.RoleRepository;
import ro.ubbcluj.util.ValidationUtil;

/**
 * This class contains all the business logic
 */
@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private PersonRepository personRepository;
    @Autowired
    private AccountRepository accountRepository;
    @Autowired
    private RoleRepository roleRepository;

    /**
     * Method returns a user by username
     *
     * @param username
     * @return
     */
    @Override
    @Transactional(readOnly = true)
    public UserDTO findByUsername(String username) {
        ValidationUtil.notNull(username);

        Account account = accountRepository.findByUsername(username);
        ValidationUtil.notNull(account);

        Person person = account.getPerson();

        return UserDTO.builder()
                .id(account.getId())
                .username(account.getUsername())
                .password(account.getPassword())
                .firstName(person.getFirstName())
                .lastName(person.getLastName())
                .email(person.getEmail())
                .role(person.getRole().getRole())
                .skills(person.getSkills())
                .registrationDate(account.getRegistrationDate())
                .active(person.isActive())
                .build();
    }

    @Override
    @Transactional
    public boolean checkUsername(String username) {
        ValidationUtil.notNull(username);

        Account account = accountRepository.findByUsername(username);

        return !ObjectUtils.isEmpty(account);
    }

    @Override
    @Transactional
    public void createUser(ChildDTO childDTO) {
        ValidationUtil.notNull(childDTO);

        Person person = getPerson(childDTO);

        personRepository.save(person);
        Account account = getAccount(childDTO, person);
        accountRepository.save(account);
    }

    private Person getPerson(ChildDTO childDTO) {
        ValidationUtil.notNull(childDTO);

        Person person = UserConverter.convertToEntityPerson(childDTO);
        person.setActive(true);

        person.setRole(roleRepository.findByRole(RoleEnum.PRESCHOOLAR));

        return person;
    }

    private Account getAccount(ChildDTO childDTO, Person person) {
        ValidationUtil.notNull(childDTO);
        ValidationUtil.notNull(person);

        Account account = UserConverter.convertToEntityAccount(childDTO);
        account.setPerson(person);
        account.setActive(true);
        return account;
    }


}
