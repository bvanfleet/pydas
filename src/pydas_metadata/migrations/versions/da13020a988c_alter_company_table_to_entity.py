# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""alter_company_table_to_entity

Revision ID: da13020a988c
Revises: f73a9aa46c77
Create Date: 2021-11-09 18:18:41.359841

When applied, this revision will change all uses of Company to Entity. Company.Symbol will become
Entity.Identifier and Company.Market will become Entity.Category.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da13020a988c'
down_revision = 'f73a9aa46c77'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("companybase") as batch_op:
        batch_op.alter_column("Symbol",
                              new_column_name="Identifier",
                              existing_type=sa.String(10))
        batch_op.alter_column("Market",
                              new_column_name="Category",
                              existing_type=sa.String(50))
                              
    batch_op.rename_table("companybase", "entitybase")

    with op.batch_alter_table("companyfeaturebase") as bulk_op:
        bulk_op.alter_column("CompanyFeatureID",
                             new_column_name="EntityFeatureID",
                             existing_type=sa.Integer())
        bulk_op.alter_column("CompanySymbol",
                             new_column_name="EntityID",
                             existing_type=sa.String(50))

    op.rename_table("companyfeaturebase", "entityfeaturebase")

    op.alter_column("optionbase",
                    "CompanySymbol",
                    new_column_name="EntityID",
                    existing_type=sa.String(50))


def downgrade():
    op.alter_column("optionbase",
                    "EntityID",
                    new_column_name="CompanySymbol",
                    existing_type=sa.String(50))
                    
    with op.batch_alter_table("entityfeaturebase") as bulk_op:
        bulk_op.alter_column("EntityFeatureID",
                             new_column_name="CompanyFeatureID",
                             existing_type=sa.Integer())
        bulk_op.alter_column("EntityID",
                             new_column_name="CompanySymbol",
                             existing_type=sa.String(50))

    op.rename_table("entityfeaturebase", "companyfeaturebase")

    with op.batch_alter_table("entitybase") as batch_op:
        batch_op.alter_column("Identifier",
                              new_column_name="Symbol",
                              existing_type=sa.String(10))
        batch_op.alter_column("Category",
                              new_column_name="Market",
                              existing_type=sa.String(50))
                              
    batch_op.rename_table("entitybase", "companybase")
