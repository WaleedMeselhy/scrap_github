"""make repo_name and repo_url unique

Revision ID: 496e87d66cb0
Revises: 79b99157bae5
Create Date: 2019-10-06 21:08:13.532405

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils



# revision identifiers, used by Alembic.
revision = '496e87d66cb0'
down_revision = '79b99157bae5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'repo', ['repo_url'])
    op.create_unique_constraint(None, 'repo', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'repo', type_='unique')
    op.drop_constraint(None, 'repo', type_='unique')
    # ### end Alembic commands ###
