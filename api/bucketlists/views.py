from flask_restx import Namespace,Resource,fields
from ..models.bucketlists import Bucketlist
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models.users import User
from ..utils import db


bucketlist_namespace=Namespace('bucketlists',description="a namespace for bucketlists")



bucketlist_model=bucketlist_namespace.model(
    'Bucketlist',{
        'bucket_id':fields.Integer(description="An id"),
        'name':fields.String(description="Name of the bucket list"),
        'date_created':fields.DateTime(description="date of creation of the bucket list"),
        'date_modified':fields.DateTime(description="date of modification of the bucket list"),
        'created_by':fields.Integer(description="user that created the bucket list")
    
    }

)


@bucketlist_namespace.route('/')
class BucketlistGetCreate(Resource):

    @bucketlist_namespace.expect(bucketlist_model)
    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="Create a new bucket list"
    )
    @jwt_required()
    def post(self):
        """
           Create a new bucket list
        """

        username=get_jwt_identity()

        current_user=User.query.filter_by(username=username).first()
        

        data=bucketlist_namespace.payload

        new_bucketlist=Bucketlist(
            name=data['name'],
            date_created=data['date_created'],
            
        )

        new_bucketlist.created_by=current_user

        new_bucketlist.save()

        return new_bucketlist , HTTPStatus.CREATED

    @bucketlist_namespace.marshal_with(bucketlist_model)

    @bucketlist_namespace.doc(
        description="List all the created bucket lists"
    )
    @jwt_required()
    def get(self):

        """
           List all the created bucket lists
        """
        bucketlists=Bucketlist.query.all()

        return bucketlists ,HTTPStatus.OK

@bucketlist_namespace.route('/<int:bucketlist_id>')
class GetUpdateDelete(Resource):


    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="Get single bucket list",
        params={
            "bucketlist_id":"An ID for a given bucketlist"

        }
    )
    @jwt_required()
    def get(self,bucketlist_id):
        """
           Get single bucket list
        """
        bucketlist=Bucketlist.get_by_id(bucketlist_id)

        return bucketlist ,HTTPStatus.OK

    @bucketlist_namespace.expect(bucketlist_model)
    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="Update this bucket list",
        params={
            "bucketlist_id":"An ID for a given bucketlist"

        }
    )
    @jwt_required()
    def put(self,bucketlist_id):
        """
           Update this bucket list
        """
        

        bucketlist_to_update=Bucketlist.get_by_id(bucketlist_id)

        data=bucketlist_namespace.payload

        bucketlist_to_update.name=data['name']
        bucketlist_to_update.date_created=data['date_created']
        bucketlist_to_update.date_modified=data['date_modified']
        bucketlist_to_update.created_by=data['created_by']

        db.session.commit()

        return bucketlist_to_update, HTTPStatus.OK


    @jwt_required()
    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="delete this single bucket list",
        params={
            "bucketlist_id":"An ID for a given bucketlist"

        }
    )
    def delete(self,bucketlist_id):
        """
           Delete this single bucket list
        """
        bucketlist_to_delete=Bucketlist.get_by_id(bucketlist_id)

        bucketlist_to_delete.delete()

        return bucketlist_to_delete, HTTPStatus.OK


@bucketlist_namespace.route('/<int:bucketlist_id>/items')
@bucketlist_namespace.doc(
        description="create a new item in the bucket list",
        params={
            "bucketlist_id":"An ID for a given bucketlist"

        }
    )
class Get(Resource):
    
    def post(self,bucketlist_id,item):
        """
            Create a new item in bucket list        
        """
        pass



@bucketlist_namespace.route('/<int:bucketlist_id>/items/<int:item_id>')

class UpdateDelete(Resource):

    @bucketlist_namespace.doc(
        description="Update a bucket list item",
        params={
            "bucketlist_id":"An ID for a given bucketlist",
            "item_id":"An item ID"

        }
    )

    def put(self,bucketlist_id,item,item_id):
        """
            Update a bucket list item
        """
        pass
    
    @bucketlist_namespace.doc(
        description="Delete an item in a bucket list",
         params={
            "bucketlist_id":"An ID for a given bucketlist",
            "item_id":"An item ID"

        }
    )
    def delete(self,bucketlist_id,item,item_id):
        """
            Delete an item in a bucket list
        """
        pass
