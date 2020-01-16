package ro.ubbcluj.model.filters;

import lombok.Getter;
import lombok.Setter;

/**
 * This class is used to filter rooms based on the facilities
 */
@Getter
@Setter
public class RoomFilter {

    private Boolean smoking;
    private Boolean petFriendly;

}
