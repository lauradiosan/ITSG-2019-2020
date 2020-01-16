package ro.ubbcluj.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QPerson is a Querydsl query type for Person
 */
@Generated("com.querydsl.codegen.EntitySerializer")
public class QPerson extends EntityPathBase<Person> {

    private static final long serialVersionUID = 295811572L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QPerson person = new QPerson("person");

    public final QAccount account;

    public final BooleanPath active = createBoolean("active");

    public final StringPath address = createString("address");

    public final StringPath bio = createString("bio");

    public final DateTimePath<java.util.Date> birthDate = createDateTime("birthDate", java.util.Date.class);

    public final StringPath email = createString("email");

    public final StringPath firstName = createString("firstName");

    public final EnumPath<ro.ubbcluj.enums.GenderEnum> gender = createEnum("gender", ro.ubbcluj.enums.GenderEnum.class);

    public final NumberPath<Long> id = createNumber("id", Long.class);

    public final StringPath lastName = createString("lastName");

    public final QRole role;

    public final StringPath skills = createString("skills");

    public QPerson(String variable) {
        this(Person.class, forVariable(variable), INITS);
    }

    public QPerson(Path<? extends Person> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QPerson(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QPerson(PathMetadata metadata, PathInits inits) {
        this(Person.class, metadata, inits);
    }

    public QPerson(Class<? extends Person> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.account = inits.isInitialized("account") ? new QAccount(forProperty("account"), inits.get("account")) : null;
        this.role = inits.isInitialized("role") ? new QRole(forProperty("role")) : null;
    }

}

