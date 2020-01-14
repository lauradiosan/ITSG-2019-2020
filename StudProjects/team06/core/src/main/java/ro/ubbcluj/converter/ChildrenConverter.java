package ro.ubbcluj.converter;

import org.springframework.data.domain.Page;
import ro.ubbcluj.dto.ChildDTO;
import ro.ubbcluj.entity.Person;

import java.util.List;
import java.util.stream.Collectors;

/**
 * @author dianat2
 */
public class ChildrenConverter {

    public static List<ChildDTO> toChildDtoList(List<Person> people) {
        return people.stream()
                .map(ChildrenConverter::toChildDto)
                .collect(Collectors.toList());
    }

    public static Page<ChildDTO> convertToDTOPage(Page<Person> documentPage) {
        return documentPage.map(ChildrenConverter::toChildDto);
    }

    private static ChildDTO toChildDto(Person person) {
        return ChildDTO.builder()
                .firstName(person.getFirstName())
                .lastName(person.getLastName())
                .build();
    }

}
