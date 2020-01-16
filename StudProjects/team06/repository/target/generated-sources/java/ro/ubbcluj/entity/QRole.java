package ro.ubbcluj.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QRole is a Querydsl query type for Role
 */
@Generated("com.querydsl.codegen.EntitySerializer")
public class QRole extends EntityPathBase<Role> {

    private static final long serialVersionUID = -388449579L;

    public static final QRole role1 = new QRole("role1");

    public final NumberPath<Long> id = createNumber("id", Long.class);

    public final ListPath<Person, QPerson> person = this.<Person, QPerson>createList("person", Person.class, QPerson.class, PathInits.DIRECT2);

    public final EnumPath<ro.ubbcluj.enums.RoleEnum> role = createEnum("role", ro.ubbcluj.enums.RoleEnum.class);

    public QRole(String variable) {
        super(Role.class, forVariable(variable));
    }

    public QRole(Path<? extends Role> path) {
        super(path.getType(), path.getMetadata());
    }

    public QRole(PathMetadata metadata) {
        super(Role.class, metadata);
    }

}

