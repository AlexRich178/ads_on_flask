import flask
from flask import Flask, request
from sqlalchemy import create_engine, Column, String, DateTime, func, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask.views import MethodView

ad_service = Flask('ad_service')
Base = declarative_base()
engine = create_engine('postgresql://alex:123456@127.0.0.1:5432/flask')
Session = sessionmaker(bind=engine)


class Errors(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@ad_service.errorhandler(Errors)
def err_handler(er: Errors):
    response = flask.jsonify({'status': 'error', 'message': er.message})
    response.status_code = er.status_code
    return response


class Ads(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True)
    header = Column(String(64), nullable=False, unique=True)
    descriprion = Column(String(256), nullable=False)
    create_time = Column(DateTime, server_default=func.now())
    owner = Column(String(24), nullable=False)


Base.metadata.create_all(engine)


def get_ad(session, ad_id):
    ad = session.query(Ads).get(ad_id)
    if ad is None:
        raise Errors(404, 'ad does not exist')
    else:
        return ad


class AdsView(MethodView):

    def get(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            return {
                'header': ad.header,
                'description': ad.descriprion
            }

    def post(self):
        ads_data = request.json
        with Session() as session:
            new_ad = Ads(header=ads_data['header'], descriprion=ads_data['descriprion'], owner=ads_data['owner'])
            session.add(new_ad)
            session.commit()
            return flask.jsonify({'header': new_ad.header, 'created_time': new_ad.create_time})

    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            session.delete(ad)
            session.commit()
            return flask.jsonify({'status': 'DELETE COMPLETE'})

    def patch(self, ad_id):
        ad_data = request.json
        with Session() as session:
            ad = get_ad(session, ad_id)
            for key, value in ad_data.items():
                setattr(ad, key, value)
            session.commit()
        return flask.jsonify({'status': 'OK'})


ad_service.add_url_rule('/ads', view_func=AdsView.as_view('ads'), methods=['POST'])
ad_service.add_url_rule('/ads/<int:ad_id>', view_func=AdsView.as_view('ads_get'), methods=['GET', 'PATCH', 'DELETE'])
ad_service.run()
