"""Added repo table

Revision ID: 170af0cf0285
Revises: 
Create Date: 2019-10-06 10:33:41.733444

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils



# revision identifiers, used by Alembic.
revision = '170af0cf0285'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dependencies',
    sa.Column('repo_dependent_id', sa.Integer(), nullable=False),
    sa.Column('repo_dependency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['repo_dependency_id'], ['repo.id'], ),
    sa.ForeignKeyConstraint(['repo_dependent_id'], ['repo.id'], ),
    sa.PrimaryKeyConstraint('repo_dependent_id', 'repo_dependency_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dependencies')
    op.drop_table('repo')
    # ### end Alembic commands ###